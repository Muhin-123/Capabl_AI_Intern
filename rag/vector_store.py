from functools import lru_cache

from langchain_community.vectorstores import FAISS

from rag.chunking import split_text
from rag.embeddings import get_embedding_model


@lru_cache(maxsize=3)
def _get_embedding_model_cached():
    """
    Cache the embedding model so it does not need to be
    initialized repeatedly.
    """

    return get_embedding_model()


def create_vector_store_from_text(
    text: str,
    metadata=None,
    content_units=None,
):
    """
    Create a FAISS vector store while preserving metadata
    for source/page/slide tracking.
    """

    documents = split_text(
        text=text,
        metadata=metadata,
        content_units=content_units,
    )

    if not documents:

        raise ValueError(
            "No text could be extracted from the document."
        )

    embedding_model = (
        _get_embedding_model_cached()
    )

    vector_store = FAISS.from_documents(
        documents,
        embedding_model,
    )

    return vector_store