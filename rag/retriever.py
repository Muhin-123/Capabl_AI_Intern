from rag.vector_store import create_vector_store_from_text


def retrieve_documents(question: str, document_text: str, k: int = 3):
    """Retrieve the most relevant chunks from the uploaded document."""

    vector_store = create_vector_store_from_text(document_text)

    results = vector_store.similarity_search(
        question,
        k=k,
    )

    return results


if __name__ == "__main__":
    question = "What is Second Normal Form?"

    sample_text = """
    Second Normal Form (2NF) requires a table to be in First Normal Form
    and removes partial dependency.
    """

    results = retrieve_documents(
        question,
        sample_text,
        k=3,
    )

    print("\nRetrieved information:\n")

    for i, document in enumerate(results, start=1):
        print(f"--- Result {i} ---")
        print(document.page_content)