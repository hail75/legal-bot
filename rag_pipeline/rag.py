from __future__ import annotations

from fastapi import UploadFile
from lightrag import LightRAG
from lightrag.llm.openai import gpt_4o_mini_complete
from lightrag.llm.openai import openai_embed


class RAG:
    def __init__(self, user_id: int):
        self.pipeline = LightRAG(
            working_dir=f'data/{user_id}',
            embedding_func=openai_embed,
            llm_model_func=gpt_4o_mini_complete,
        )

    async def insert_file(self, file: UploadFile):
        await self.pipeline.initialize_storages()

        ...
