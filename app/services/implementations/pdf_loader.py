from typing import List
import glob
import os
from langchain.schema import Document
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from app.services.interfaces.document_loader import DocumentLoader
from langchain.text_splitter import TokenTextSplitter, CharacterTextSplitter
from app.config import get_settings


class PDFLoader(DocumentLoader):
    def load_documents(self, path: str) -> List[Document]:
        print(f"Loading documents from path: {path}")
        folders = glob.glob(path)
        documents = []
        for folder in folders:
            if os.path.isdir(folder):
                loader = DirectoryLoader(
                    folder, glob="**/*.pdf", loader_cls=PyPDFLoader
                )
                docs = loader.load()
                documents.extend(docs)
        text_splitter = self.create_text_splitter()
        chunked_documents = text_splitter.split_documents(documents)
        return chunked_documents

    def create_text_splitter(self):
        settings = get_settings()
        return CharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separator="\n",
        )
