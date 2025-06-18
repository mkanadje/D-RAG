from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from app.services.rag_service import RAGService
import ipdb
from app.config import get_settings
import os
import shutil

app = FastAPI()
rag_service = None


class ChatRequest(BaseModel):
    message: str


@app.get("/rag_exists")
async def rag_exists():
    global rag_service
    return {"exists": rag_service is not None}


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    global rag_service
    if not rag_service:
        raise HTTPException(status_code=400, message="RAG is not initialized.")
    answer = rag_service.query(request.message)
    return {"answer": answer}


@app.post("/build")
async def build_rag_db():
    global rag_service
    rag_service = RAGService()
    rag_service.build_pipeline()
    return {"status": "RAG database built successfully."}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    settings = get_settings()
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PFD files are allowed.")
    os.makedirs(settings.DATA_FOLDER_PATH, exist_ok=True)
    print(f"Uploading file: {file.filename} to {settings.DATA_FOLDER_PATH}")
    file_path = os.path.join(settings.DATA_FOLDER_PATH, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "status": "File uploaded successfully."}
