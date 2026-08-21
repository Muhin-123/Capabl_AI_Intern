from urllib import response

from rag.retriever import retrieve_documents
from rag.llm import get_llm


def generate_answer(question: str):
    # Step 1: Retrieve relevant chunks from FAISS
    documents = retrieve_documents(question, k=3)

    # Step 2: Combine retrieved chunks
    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    # Step 3: Get Gemini
    llm = get_llm()

    # Step 4: Create RAG prompt
    prompt = f"""
You are an academic AI assistant.

Answer the student's question using ONLY the academic
context provided below.

Rules:
- Use the retrieved context as your primary source.
- Do not invent facts that are not supported by the context.
- Explain the answer clearly and simply.
- Give examples when useful.
- If the context does not contain enough information,
  clearly say that the uploaded material does not contain
  enough information to answer the question.

ACADEMIC CONTEXT:
{context}

STUDENT QUESTION:
{question}

ANSWER:
"""

    # Step 5: Generate answer
    response = llm.invoke(prompt)

    if isinstance(response.content, str):
        answer = response.content
    else:
        answer = "".join(
            block.get("text", "")
            for block in response.content
            if isinstance(block, dict)
    )

    return answer, documents


if __name__ == "__main__":
    question = "What is Second Normal Form?"

    answer, sources = generate_answer(question)

    print("\n==============================")
    print("ANSWER")
    print("==============================\n")

    print(answer)

    print("\n==============================")
    print("SOURCES")
    print("==============================\n")

    for i, document in enumerate(sources, start=1):
        print(f"--- Source {i} ---")
        print(document.page_content)
        print()