from rag.vector_store import (
    create_vector_store_from_text,
)


def retrieve_documents(
    question: str,
    document_text: str,
    k: int = 3,
    metadata=None,
    content_units=None,
):
    """
    Retrieve the most relevant chunks from the uploaded
    document while preserving source metadata.
    """

    vector_store = (
        create_vector_store_from_text(
            text=document_text,
            metadata=metadata,
            content_units=content_units,
        )
    )

    results = vector_store.similarity_search(
        question,
        k=k,
    )

    return results


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    question = (
        "What is Second Normal Form?"
    )

    sample_text = """
    Second Normal Form (2NF) requires a table to be
    in First Normal Form and removes partial dependency.
    """

    results = retrieve_documents(
        question=question,
        document_text=sample_text,
        k=3,
    )

    print(
        "\nRetrieved information:\n"
    )

    for i, document in enumerate(
        results,
        start=1,
    ):

        print(
            f"--- Result {i} ---"
        )

        print(
            document.page_content
        )

        print(
            "Metadata:",
            document.metadata,
        )