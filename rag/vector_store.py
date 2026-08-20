from langchain_community.vectorstores import FAISS

from rag.chunking import load_and_split_text
from rag.embeddings import get_embedding_model


def create_vector_store(file_path: str):
    """Create a FAISS vector store from a text file."""

    chunks = load_and_split_text(file_path)

    embedding_model = get_embedding_model()

    vector_store = FAISS.from_texts(
        chunks,
        embedding_model
    )

    return vector_store