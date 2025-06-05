from fastapi import FastAPI, Request
from pydantic import BaseModel
from engine import build_rag_pipeline

app = FastAPI()

conversation_chain = build_rag_pipeline()


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    response = conversation_chain({"question": request.message})
    return {"answer": response["answer"]}
