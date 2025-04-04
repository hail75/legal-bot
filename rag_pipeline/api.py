from __future__ import annotations

from fastapi import FastAPI
from fastapi import File
from fastapi import Form
from fastapi import UploadFile


app = FastAPI()


@app.post('/insert_file')
async def insert_file(
    file: UploadFile = File(...),
    user_id: int = Form(...),
):
    ...
