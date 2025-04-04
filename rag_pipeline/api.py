from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi import File
from fastapi import Form
from fastapi import UploadFile
from fastapi.responses import JSONResponse
from rag import RAG


app = FastAPI()
app.state.rag_instances = {}


@app.post('/insert_file')
async def insert_file(
    file: UploadFile = File(...),
    user_id: str = Form(...),
):
    file_path = await save_file(file, user_id)

    if user_id not in app.state.rag_instances:
        app.state.rag_instances[user_id] = RAG(user_id)
        await app.state.rag_instances[user_id].ainit()

    rag = app.state.rag_instances[user_id]
    await rag.insert_file(file_path)
    return JSONResponse(
        {
            'status': 'success', 'message': 'File inserted successfully'
        }
    )

# @app.post('/query')
# async def query(
#     query: str = Form(...),
#     user_id: str = Form(...),
# ):
#     if user_id not in app.state.rag_instances:
#         return JSONResponse(
#             {
#                 "status": "error",
#                 "message": "No RAG instance found for this user"
#             }
#         )


async def save_file(file: UploadFile, user_id: str) -> str:
    """Save the file locally."""
    file_path = os.path.join('uploaded', user_id, file.filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as f:
        f.write(await file.read())
    return file_path
