from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.services.rag_service import RAGService
import ipdb

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
