from abc import ABC, abstractmethod
from typing import List
from langchain.schema import (
    Document,
)  # TODO: Replace with a more general document schema


class DocumentStore(ABC):
    @abstractmethod
    def store_documents(self, documents: List[Document]) -> None:
        pass

    @abstractmethod
    def get_retriever(self):  # TODO: Define a more specific return_type (protocol)
        pass
