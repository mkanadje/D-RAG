import os
import glob
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)
import re
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from IPython.display import Markdown, display
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter
import shutil


def load_documents(folder_path=None):
    load_dotenv()
    if folder_path is None:
        folder_path = os.getenv("DATA_FOLDER_PATH", folder_path)
    folders = glob.glob(folder_path)
    documents = []
    for folder in folders:
        if os.path.isdir(folder):
            # loader = DirectoryLoader(folder, glob="**/*.pdf", loader_cls=PyPDFLoader)
            loader = SimpleDirectoryReader(folder)
            doc = loader.load_data()
            documents.extend(doc)
    return documents


def update_metadata(documents):
    prev_match = ["other_content"]
    for doc in documents:
        content = getattr(doc, "text", None) or getattr(doc, "page_content", "")
        matches = re.findall("Chpater\n\\d+", content)
        if len(matches) > 0:
            matches = [m.replace("\n", " ") for m in matches]
            prev_match = matches
        else:
            matches = prev_match
        matches_str = ",".join(matches)
        if not hasattr(doc, "metadata") or doc.metadata is None:
            doc.metadata = {}
        doc.metadata["chapters"] = matches_str
    return documents


def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    text_splitter = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    nodes = text_splitter.get_nodes_from_documents(documents)
    return nodes


def load_api_keys():
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    os.environ["MODEL_NAME"] = os.getenv("MODEL_NAME")


def build_vector_store(nodes, persist_folder=None):
    load_dotenv()
    if persist_folder is None:
        persist_folder = os.getenv("VECTOR_DB_PATH", persist_folder)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    if os.path.exists(persist_folder):
        print(f"Removing existing vector store at {persist_folder}")
        shutil.rmtree(persist_folder)
    print(f"Creating vector store at {persist_folder}")
    vector_store_index = VectorStoreIndex(
        nodes=nodes, embed_model=embeddings, persist_dir=persist_folder
    )
    return vector_store_index


def build_conversation_chain(vector_store, model_name):
    # llm = ChatOpenAI(temperature=0.7, model_name=model_name)
    llm = OpenAI(model_name=model_name, temperature=0.7)
    # memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    # retriever = vector_store.as_retriever()
    # conversation_chain = ConversationalRetrievalChain.from_llm(
    # llm=llm, retriever=retriever, memory=memory
    # )
    query_engine = vector_store.as_query_engine(llm=llm)
    return query_engine


def build_rag_pipeline(documents_folder=None, persist_folder=None):
    load_api_keys()
    print("Loaded API keys...")
    documents = load_documents(folder_path=documents_folder)
    print(f"Loaded {len(documents)} documents.")
    if len(documents) > 0:
        documents = update_metadata(documents)
        print("Updated metadata for documents")
        chunks = split_documents(documents)
        print(f"Split documents into {len(chunks)} chunks.")
        vector_store = build_vector_store(chunks, persist_folder=persist_folder)
        print("Built vector store.")
        conversation_chain = build_conversation_chain(
            vector_store, os.getenv("MODEL_NAME")
        )
        print("Built conversation chain.")
        return conversation_chain
    else:
        raise Warning("No documents found in the specified folder.")


def run():
    conversation_chain = build_rag_pipeline()
    print("RAG pipeline is ready. You can start asking questions.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the conversation.")
            break
        response = conversation_chain.query({"question": user_input})
        print(f'Bot: {response["answer"]}')


if __name__ == "__main__":
    run()
