from functools import lru_cache

from langchain_community.vectorstores import FAISS

from rag.chunking import split_text
from rag.embeddings import get_embedding_model


@lru_cache(maxsize=3)
def create_vector_store_from_text(text: str):
    """Create and cache a FAISS vector store from document text."""

    chunks = split_text(text)

    if not chunks:
        raise ValueError(
            "No text could be extracted from the document."
        )

    embedding_model = get_embedding_model()

    vector_store = FAISS.from_texts(
        chunks,
        embedding_model,
    )

    return vector_store