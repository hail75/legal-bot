from __future__ import annotations

import mimetypes
import os

import aiohttp
from telegram import Update
from telegram.ext import ApplicationBuilder
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes
from telegram.ext import filters
from telegram.ext import MessageHandler


class TelegramBot:
    def __init__(self, token: str, rag_url: str):
        self.app = ApplicationBuilder().token(token).build()
        self.rag_url = rag_url
        self._add_handlers()

    def _add_handlers(self):
        """Add handlers to the application."""
        self.app.add_handler(
            CommandHandler(
                'start',
                self.start_handler,
            )
        )
        self.app.add_handler(
            MessageHandler(
                filters.Document.ALL,
                self.file_handler,
            )
        )
        self.app.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.Document.ALL & ~filters.COMMAND,
                self.text_handler,
            )
        )

    def run(self):
        """Run the bot."""
        self.app.run_polling(
            drop_pending_updates=True,
            allowed_updates=Update.ALL_TYPES,
        )

    async def start_handler(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        """Sends a message when the command /start is issued."""
        if context.chat_data.get('started', False):
            await update.message.reply_text(
                'Bạn đã bắt đầu cuộc trò chuyện rồi.'
            )
            return

        user = update.effective_user
        context.chat_data['started'] = True
        context.chat_data['files_received'] = 0
        await update.message.reply_text(
            f'Xin chào {user.first_name}! Vui lòng upload file để tiếp tục.',
        )

    async def file_handler(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        """Handles the uploaded file."""
        if not context.chat_data.get('started', False):
            await update.message.reply_text(
                'Vui lòng bắt đầu cuộc trò chuyện trước khi upload file.'
            )
            return

        if context.chat_data.get('processing_file', False):
            await update.message.reply_text(
                'Đang xử lý file. Vui lòng đợi một chút. 😡'
            )
            return

        if context.chat_data.get('processing_query', False):
            await update.message.reply_text(
                'Đang xử lý yêu cầu. Vui lòng đợi một chút. 😡'
            )

        # Check for file extension
        file = update.message.document
        if not file.file_name.endswith('.docx'):
            await update.message.reply_text(
                'Vui lòng upload file có định dạng .docx.'
            )
            return
        else:
            await update.message.reply_text(
                'File đã được nhận. Đang trích xuất thông tin từ file...'
            )
            context.chat_data['processing_file'] = True

            # Save the file locally
            file_object = await self.app.bot.get_file(file.file_id)
            file_path = os.path.join('uploaded', str(
                update.effective_user.id), file.file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            await file_object.download_to_drive(file_path)

            response = await self._send_file_to_rag_pipeline(
                file.file_name, update.effective_user.id)
            if response.get('status') != 'success':
                await update.message.reply_text(
                    'Có lỗi xảy ra khi trích xuất thông tin từ file. '
                    'Vui lòng thử lại.'
                )
                context.chat_data['processing_file'] = False
                return

            await update.message.reply_text(
                'Trích xuất thông tin thành công. '
                'Từ bây giờ bạn có thể '
                'hỏi, tra cứu thông tin hoặc yêu cầu tóm tắt, v.v.')
            context.chat_data['files_received'] += 1
            context.chat_data['processing_file'] = False

    async def text_handler(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        """Handles the text messages."""
        if not context.chat_data.get('started', False):
            await update.message.reply_text(
                'Vui lòng bắt đầu cuộc trò chuyện trước khi gửi tin nhắn.'
            )
            return

        if context.chat_data.get('processing_file', False):
            await update.message.reply_text(
                'Đang xử lý file. Vui lòng đợi một chút. 😡'
            )
            return

        if context.chat_data.get('files_received', 0) == 0:
            await update.message.reply_text(
                'Vui lòng upload file trước khi gửi tin nhắn.'
            )
            return

        if context.chat_data.get('processing_query', False):
            await update.message.reply_text(
                'Đang xử lý yêu cầu. Vui lòng đợi một chút. 😡'
            )
        # Process the text message
        query = update.message.text
        context.chat_data['processing_query'] = True
        await update.message.reply_text(
            self._send_query_to_rag_pipeline(query, update.effective_user.id)
        )
        context.chat_data['processing_query'] = False

    async def _send_file_to_rag_pipeline(self, file_path: str, user_id: int):
        # TODO: Send POST request to RAG pipeline API
        async with aiohttp.ClientSession() as session:
            form = aiohttp.FormData()
            file_name = os.path.basename(file_path)
            mime_type, _ = mimetypes.guess_type(file_name)

            form.add_field(
                'file',
                open(file_path, 'rb'),
                filename=file_name,
                content_type=mime_type,
            )
            form.add_field('user_id', str(user_id))

            async with session.post(
                f'{self.rag_url}/insert_file',
                data=form,
            ) as response:
                response_json = await response.json()
                os.remove(file_path)
                return response_json

    def _send_query_to_rag_pipeline(self, query: str, user_id: int):
        # TODO
        ...


if __name__ == '__main__':
    bot = TelegramBot(
        token=os.environ['TELEGRAM_BOT_TOKEN'],
        rag_url=os.environ['RAG_PIPELINE_URL'],
    )
    bot.run()
