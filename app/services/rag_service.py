from typing import Optional
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from app.services.implementations.chroma_store import ChromaDocumentStore
from app.services.implementations.pdf_loader import PDFLoader
from app.config import get_settings
import ipdb


class RAGService:
    def __init__(self):
        self.settings = get_settings()
        self.document_store = ChromaDocumentStore()
        self.document_loader = PDFLoader()
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        self.chain = None

    def build_pipeline(self):
        documents = self.document_loader.load_documents(self.settings.DATA_FOLDER_PATH)
        if not documents:
            raise ValueError("No documents found in the specified data folder.")
        self.document_store.store_documents(documents)

        llm = ChatOpenAI(
            temperature=self.settings.TEMPERATURE,
            model_name=self.settings.MODEL_NAME,
            api_key=self.settings.OPENAI_API_KEY,
        )

        self.chain = ConversationalRetrievalChain.from_llm(
            llm=llm, retriever=self.document_store.get_retriever(), memory=self.memory
        )

    def query(self, question: str) -> Optional[str]:
        if not self.chain:
            raise RuntimeError("Pipeline not initialized.")
        response = self.chain({"question": question})
        return response["answer"]
