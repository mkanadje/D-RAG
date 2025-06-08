from abc import ABC, abstractmethod
from typing import List

# Assuming the Document class is defined as per LangChain's schema
from langchain.schema import Document  # TODO: Replace with a more general document


class DocumentLoader(ABC):
    @abstractmethod
    def load_documents(self, path: str) -> List[Document]:
        pass
