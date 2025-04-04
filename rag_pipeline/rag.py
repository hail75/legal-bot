from __future__ import annotations

import docx2txt
from lightrag import LightRAG
from lightrag.kg.shared_storage import initialize_pipeline_status
from lightrag.llm.openai import gpt_4o_mini_complete
from lightrag.llm.openai import openai_embed


class RAG:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.pipeline = LightRAG(
            working_dir=f'data/{self.user_id}',
            embedding_func=openai_embed,
            llm_model_func=gpt_4o_mini_complete,
        )

    async def ainit(self):
        await self.pipeline.initialize_storages()
        await initialize_pipeline_status()

    async def insert_file(self, file_path: str):
        text = docx2txt.process(file_path)
        await self.pipeline.ainsert(text)
