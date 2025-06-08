from typing import List, Optional
import shutil
import os
from langchain.schema import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from app.services.interfaces.document_store import DocumentStore
from app.config import get_settings


class ChromaDocumentStore(DocumentStore):
    def __init__(self, persist_folder: Optional[str] = None):
        self.settings = get_settings()
        self.persist_folder = persist_folder or self.settings.VECTOR_DB_PATH
        self.embeddings = (
            OpenAIEmbeddings()
        )  # Embeddings are at store level to avoid re-instantiation
        self.vector_store = None

    def store_documents(self, documents: List[Document]) -> None:
        # TODO: This method completely overwrites the existing vector store.
        # Implement update or append functionality
        if os.path.exists(self.persist_folder):
            shutil.rmtree(self.persist_folder)
        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_folder,
        )

    def get_retriever(self):
        if not self.vector_store:
            raise RuntimeError("No documents stored yet.")
        return self.vector_store.as_retriever()
