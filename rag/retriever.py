from rag.vector_store import create_vector_store


def retrieve_documents(question: str, k: int = 3):
    """Retrieve the most relevant chunks for a question."""

    vector_store = create_vector_store("data/sample.txt")

    results = vector_store.similarity_search(
        question,
        k=k
    )

    return results


if __name__ == "__main__":
    question = "What is Second Normal Form?"

    results = retrieve_documents(question)

    print("\nRetrieved information:\n")

    for i, document in enumerate(results, start=1):
        print(f"--- Result {i} ---")
        print(document.page_content)