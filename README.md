# RAG Chatbot with FastAPI and Streamlit

A Retrieval Augmented Generation (RAG) chatbot implementation using FastAPI for the backend API, Streamlit for the user interface, and a clean architecture approach with clear separation of interfaces and implementations.

## Features

- PDF document ingestion and processing
- Vector-based document storage using Chroma
- RAG-powered conversational AI using LangChain
- Clean architecture with interface-based design
- FastAPI backend with async endpoints
- Interactive Streamlit-based chat interface
- Docker support for containerized deployment

## Project Structure

```
.
├── app/
│   ├── main.py                    # FastAPI application and endpoints
│   ├── streamlit_app.py           # Streamlit UI application
│   ├── config.py                  # Configuration management
│   └── services/
│       ├── interfaces/            # Abstract interfaces
│       │   ├── document_loader.py
│       │   ├── document_store.py
│       │   └── ui_interface.py
│       ├── implementations/       # Concrete implementations
│       │   ├── chroma_store.py
│       │   ├── pdf_loader.py
│       │   └── streamlit_ui.py
│       └── rag_service.py         # Core RAG service implementation
├── rag/
│   ├── data/                      # Directory for source PDF documents
│   └── vector_db/                 # Vector database storage
├── Dockerfile
├── requirements.txt
├── start.sh
└── fly.toml
```

## Prerequisites

- Python 3.11+
- OpenAI API key
- PDF documents to process

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd llm_rag
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your configuration:
```env
OPENAI_API_KEY=your_api_key_here
MODEL_NAME=gpt-4-mini  # or your preferred model
BACKEND_HOST=http://localhost
BACKEND_PORT=8080
```

## Usage

1. Place your PDF documents in the `rag/data` directory.

2. Start the FastAPI backend:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

3. Start the Streamlit frontend:
```bash
streamlit run app/streamlit_app.py
```

4. Open your browser and navigate to http://localhost:8501

5. Click the "Build RAG" button to process your documents and initialize the system.

6. Start chatting with the RAG-powered chatbot!

## Docker Deployment

Build and run the application using Docker:

```bash
docker build -t rag-chatbot .
docker run -p 8080:8080 -p 8501:8501 rag-chatbot
```

## API Endpoints

- `POST /chat`: Send a message to the chatbot
- `POST /build`: Build/rebuild the RAG database
- `GET /rag_exists`: Check if RAG system is initialized

## Architecture

This project follows clean architecture principles with clear separation of concerns:

- **Interfaces**: Abstract base classes defining the contract for services
  - `DocumentLoader`: Interface for document loading operations
  - `DocumentStore`: Interface for vector storage operations
  - `UIService`: Interface for UI implementations

- **Implementations**: Concrete implementations of the interfaces
  - `PDFLoader`: PDF document loading implementation
  - `ChromaStore`: Chroma vector database implementation
  - `StreamlitUI`: Streamlit-based UI implementation

- **Services**: 
  - `RAGService`: Core service implementing the RAG pipeline using LangChain
  - Handles document processing, storage, and query operations

- **Configuration**: Environment-based configuration management with support for:
  - OpenAI API settings
  - Model parameters
  - Document processing settings
  - Server configuration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
