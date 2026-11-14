from models.vector_store import VectorStore
from services.llm_service import LLMService
from services.storage_service import S3Storage
from config import config
import os
from langchain.document_loaders import TextLoader,PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tempfile
import logging

vector_store = VectorStore(config.VECTOR_DB_PATH)
storage_service = S3Storage()
llm_service = LLMService(vector_store)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def process_document(file):
    """Process the uploaded document, split it into chunks, add to vector store, and upload to S3."""
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, file.filename)
    try:
        # Save file temporarily to a temporary directory
        file.save(temp_path)

        # Process based on file type and load the document accordingly
        # Determine the file type and load the document accordingly
        if file.filename.endswith('.txt'):
            loader = TextLoader(temp_path)
        elif file.filename.endswith('.pdf'):
            loader = PyPDFLoader(temp_path)
        else:
            raise ValueError(f"Unsupported file type")
            return {"error": "Unsupported file type. Please upload a .txt or .pdf file."}

        # Load the document
        documents = loader.load()

        # Split the document into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        text_chunks = text_splitter.split_documents(documents)

        return text_chunks

    finally:
        # Clean up the temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)
        os.rmdir(temp_dir)