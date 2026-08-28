from rag.retriever import retrieve_documents
from rag.llm import get_llm


def generate_answer(
    question: str,
    document_text: str,
    question_type: str = "theory",
    options: dict | None = None,
    marks: int | None = None,
):
    """
    Generate an academic answer using the RAG pipeline.

    question_type can be:
        - mcq
        - multiple_select
        - numerical
        - theory
    """

    # ========================================================
    # STEP 1 — RETRIEVE RELEVANT CHUNKS
    # ========================================================

    documents = retrieve_documents(
        question,
        document_text,
        k=3,
    )

    # ========================================================
    # STEP 2 — COMBINE RETRIEVED CONTEXT
    # ========================================================

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    # ========================================================
    # STEP 3 — PREPARE QUESTION INFORMATION
    # ========================================================

    question_information = question

    if options:
        question_information += "\n\nOPTIONS:\n"

        for letter, option_text in options.items():
            question_information += (
                f"{letter}. {option_text}\n"
            )

    # ========================================================
    # STEP 4 — SELECT PROMPT BASED ON QUESTION TYPE
    # ========================================================

    if question_type == "mcq":

        task_instruction = """
This is a Multiple Choice Question.

Analyze the question and the provided options.

If the uploaded academic context contains enough
information to determine the answer:

1. Identify the correct option.
2. State the option clearly.
3. Explain why it is correct.
4. Briefly explain why the other options are incorrect
   when the context supports doing so.

Do not guess when essential information is genuinely
missing. Use the information in the question and options
together with relevant academic reasoning.
"""

    elif question_type == "multiple_select":

        task_instruction = """
This is a Multiple Select Question.

Analyze all of the provided options.

Use the retrieved academic context together with the
information explicitly provided in the question and
standard academic reasoning.

1. Identify ALL correct options.
2. Clearly list the correct option letters.
3. Explain why each selected option is correct.
4. Explain why the remaining options are incorrect when
   appropriate.

Do not guess when essential information is genuinely
missing. If the question cannot be determined reliably,
clearly explain what information is missing.
"""
    elif question_type == "numerical":

        task_instruction = """
This is a Numerical Answer Type Question.

Solve the problem carefully using the information provided
in the question, the retrieved academic context, and
standard academic reasoning.

1. Identify the relevant values and given information.
2. Identify the appropriate formula, algorithm, or method.
3. Show the calculation or reasoning step by step.
4. Explain the reasoning clearly.
5. Give the final numerical answer clearly.

You may use standard mathematical formulas, algorithms,
and methods even if they are not explicitly written in
the uploaded document, provided they are directly
applicable to the question.

Do not invent missing values or unsupported assumptions.

If essential information needed to solve the problem is
genuinely missing, clearly state what information is
missing instead of guessing.
"""

    else:

        task_instruction = """
This is an academic/theoretical question.

Answer the question clearly using the provided context.

Explain the relevant concepts and give examples when
the context supports them.

Do not introduce unsupported facts.
"""

    # ========================================================
    # STEP 5 — BUILD RAG PROMPT
    # ========================================================

    prompt = f"""
You are an academic AI assistant.

Your task is to answer the student's question using ONLY
the academic context retrieved from the uploaded document.

IMPORTANT RULES:

- Use the retrieved academic context as the primary source.
- Use the information explicitly provided in the question
  and options when solving the problem.
- You may apply standard academic reasoning, calculations,
  and logical deductions to the provided information.
- Do not invent facts, values, definitions, or claims.
- You may use standard academic formulas, algorithms,
  mathematical methods, and logical reasoning when they
  are directly applicable to the information given in the
  question.
- Do not invent missing values or make unsupported
  assumptions.
- Do not claim that information came from the uploaded
  document if it was derived through reasoning.
- If essential information is genuinely missing, clearly
  state what information is missing.
- Give a clear and academically appropriate answer.
- Respect the question type.
- If the question has options, consider the options as part
  of the question.

QUESTION TYPE:
{question_type}

MARKS:
{marks if marks is not None else "Not specified"}

QUESTION:
{question_information}

QUESTION-SPECIFIC INSTRUCTIONS:
{task_instruction}

ACADEMIC CONTEXT:
{context}

ANSWER:
"""

    # ========================================================
    # STEP 6 — GENERATE ANSWER
    # ========================================================

    llm = get_llm()

    response = llm.invoke(prompt)

    # ========================================================
    # STEP 7 — EXTRACT RESPONSE TEXT
    # ========================================================

    if isinstance(response.content, str):

        answer = response.content

    else:

        answer = "".join(
            block.get("text", "")
            for block in response.content
            if isinstance(block, dict)
        )

    return answer, documents


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    question = "What is Second Normal Form?"

    document_text = """
    Second Normal Form (2NF) requires a table to be in
    First Normal Form and removes partial dependency.
    """

    answer, sources = generate_answer(
        question,
        document_text,
        question_type="theory",
    )

    print("\n==============================")
    print("ANSWER")
    print("==============================\n")

    print(answer)

    print("\n==============================")
    print("SOURCES")
    print("==============================\n")

    for i, document in enumerate(
        sources,
        start=1,
    ):

        print(f"--- Source {i} ---")
        print(document.page_content)
        print()