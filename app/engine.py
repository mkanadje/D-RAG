import os
import glob
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
import re
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from IPython.display import Markdown, display


def load_documents(folder_path=None):
    load_dotenv()
    folder_path = os.getenv("DATA_FOLDER_PATH", folder_path)
    folders = glob.glob(folder_path)
    documents = []
    for folder in folders:
        if os.path.isdir(folder):
            loader = DirectoryLoader(folder, glob="**/*.pdf", loader_cls=PyPDFLoader)
            doc = loader.load()
            documents.extend(doc)
    return documents


def update_metadata(documents):
    prev_match = ["other_content"]
    for doc in documents:
        matches = re.findall("Chpater\n\\d+", doc.page_content)
        if len(matches) > 0:
            matches = [m.replace("\n", " ") for m in matches]
            prev_match = matches
        else:
            matches = prev_match
        matches = ",".join(matches)
        doc.metadata["chapters"] = matches
    return documents


def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    text_splitter = CharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separator="\n",
    )
    chunks = text_splitter.split_documents(documents)
    return chunks


def load_api_keys():
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    os.environ["MODEL_NAME"] = os.getenv("MODEL_NAME")


def build_vector_store(chunks, persist_folder=None):
    load_dotenv()
    persist_folder = os.getenv("VECTOR_DB_PATH", persist_folder)
    embeddings = OpenAIEmbeddings()
    if os.path.exists(persist_folder):
        Chroma(
            persist_directory=persist_folder, embedding_function=embeddings
        ).delete_collection()
    vector_store = Chroma.from_documents(
        documents=chunks, embedding=embeddings, persist_directory=persist_folder
    )
    return vector_store


def build_conversation_chain(vector_store, model_name):
    llm = ChatOpenAI(temperature=0.7, model_name=model_name)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    retriever = vector_store.as_retriever()
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=retriever, memory=memory
    )
    return conversation_chain


def build_rag_pipeline():
    load_api_keys()
    print("Loaded API keys...")
    documents = load_documents()
    print(f"Loaded {len(documents)} documents.")
    if len(documents) > 0:
        documents = update_metadata(documents)
        print("Updated metadata for documents")
        chunks = split_documents(documents)
        print(f"Split documents into {len(chunks)} chunks.")
        vector_store = build_vector_store(chunks)
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
        response = conversation_chain.invoke({"question": user_input})
        print(f'Bot: {response["answer"]}')


if __name__ == "__main__":
    run()
