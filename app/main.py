from fastapi import FastAPI, Request
from pydantic import BaseModel
from app.engine import build_rag_pipeline

app = FastAPI()


conversation_chain = None


class ChatRequest(BaseModel):
    message: str


@app.get("/rag_exists")
async def rag_exists():
    global conversation_chain
    if conversation_chain is None:
        return {"exists": False}
    return {"exists": True}


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    global conversation_chain
    if conversation_chain is None:
        return {"error": "RAG database not built yet. Please build it first."}
    response = conversation_chain({"question": request.message})
    return {"answer": response["answer"]}


@app.post("/build")
async def build_rag_db():
    global conversation_chain
    conversation_chain = build_rag_pipeline()
    return {"status": "RAG database built successfully."}
