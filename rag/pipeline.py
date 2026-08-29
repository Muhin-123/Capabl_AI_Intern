from rag.retriever import retrieve_documents
from rag.llm import get_llm


def generate_answer(
    question: str,
    document_text: str,
    question_type=None,
    options=None,
    marks=None,
    document_metadata=None,
    content_units=None,
):
    """
    Generate an answer using retrieved academic context.

    Metadata and page/slide information are preserved
    throughout the RAG pipeline.
    """

    # ========================================================
    # STEP 1 — RETRIEVE RELEVANT CHUNKS
    # ========================================================

    documents = retrieve_documents(
        question=question,
        document_text=document_text,
        k=3,
        metadata=document_metadata,
        content_units=content_units,
    )

    # ========================================================
    # STEP 2 — COMBINE RETRIEVED CONTEXT
    # ========================================================

    context_parts = []

    for document in documents:

        context_parts.append(
            document.page_content
        )

    context = "\n\n".join(
        context_parts
    )

    # ========================================================
    # STEP 3 — GET GEMINI
    # ========================================================

    llm = get_llm()

    # ========================================================
    # STEP 4 — QUESTION TYPE INSTRUCTIONS
    # ========================================================

    task_instruction = ""

    if question_type == "numerical":

        task_instruction = """
This is a Numerical Answer Type Question.

Solve the problem using ONLY the academic context.

If the context contains enough information:

1. Identify the relevant values and formulas.
2. Show the calculation step by step.
3. Explain the reasoning clearly.
4. Give the final numerical answer clearly.

Do not invent missing values or formulas.

If the context does not contain enough information,
clearly state that the uploaded material does not
contain enough information.
"""

    elif question_type == "multiple_select":

        task_instruction = """
This is a Multiple Select Question.

Determine the correct options using ONLY the academic
context.

Do not guess the correct options if the context does
not contain enough information.

Explain why the selected options are correct.
"""

    elif question_type == "mcq":

        task_instruction = """
This is a Multiple Choice Question.

Determine the correct option using ONLY the academic
context.

Do not guess the correct option if the context does
not contain enough information.

Explain the answer clearly.
"""

    else:

        task_instruction = """
Answer the question using ONLY the academic context.

If the context contains enough information, explain
the answer clearly and academically.

If the context does not contain enough information,
clearly state that the uploaded material does not
contain enough information.
"""

    # ========================================================
    # STEP 5 — RAG PROMPT
    # ========================================================

    prompt = f"""
You are an academic AI assistant.

IMPORTANT RULES:

- Use ONLY the academic context provided below.
- The academic context is the only allowed source of facts.
- Do NOT use general knowledge outside the provided context.
- Do NOT introduce unsupported facts, formulas, values,
  assumptions, or calculations.
- Do NOT guess when the context is insufficient.
- If the context does not contain enough information,
  clearly say that the uploaded material does not contain
  enough information to answer the question.
- Give a clear and academically appropriate answer.
- Respect the question type.

{task_instruction}

ACADEMIC CONTEXT:
{context}

STUDENT QUESTION:
{question}

ANSWER:
"""

    # ========================================================
    # STEP 6 — GENERATE ANSWER
    # ========================================================

    response = llm.invoke(
        prompt
    )

    if isinstance(
        response.content,
        str,
    ):

        answer = response.content

    else:

        answer = "".join(
            block.get(
                "text",
                "",
            )
            for block in response.content
            if isinstance(
                block,
                dict,
            )
        )

    return answer, documents


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    question = (
        "What is Second Normal Form?"
    )

    document_text = """
    Second Normal Form (2NF) requires a table to be
    in First Normal Form and removes partial dependency.
    """

    answer, sources = generate_answer(
        question=question,
        document_text=document_text,
    )

    print(
        "\n=============================="
    )

    print("ANSWER")

    print(
        "==============================\n"
    )

    print(answer)

    print(
        "\n=============================="
    )

    print("SOURCES")

    print(
        "==============================\n"
    )

    for i, document in enumerate(
        sources,
        start=1,
    ):

        print(
            f"--- Source {i} ---"
        )

        print(
            document.page_content
        )

        print(
            "Metadata:",
            document.metadata,
        )

        print()