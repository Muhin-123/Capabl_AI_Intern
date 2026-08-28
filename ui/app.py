import os
import sys
import tempfile
from pathlib import Path

# ============================================================
# PROJECT PATH
# ============================================================

# Add project root to Python path before importing project modules
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# IMPORTS
# ============================================================

import streamlit as st

from components.sidebar import render_sidebar
from components.answer import render_answer
from components.sources import render_sources
from components.question_bank import render_question_bank
from document_processing.processor import process_document
from rag.pipeline import generate_answer


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Academic AI Agent",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>
        .main-title {
            font-size: 2.4rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }

        .subtitle {
            font-size: 1.05rem;
            color: #6b7280;
            margin-bottom: 1.5rem;
        }

        .section-title {
            font-size: 1.35rem;
            font-weight: 600;
            margin-top: 1rem;
            margin-bottom: 0.6rem;
        }

        .info-card {
            padding: 1rem;
            border-radius: 10px;
            border: 1px solid rgba(128, 128, 128, 0.25);
            margin-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🎓 Academic AI Agent</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Your personal AI assistant for understanding academic material."
    "</div>",
    unsafe_allow_html=True,
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

uploaded_file, subject, topic = render_sidebar()
answer = None
sources = None

# Temporary mock questions for Question Bank UI development.
# Replace with document processor output later.
mock_questions = [
    {
        "question_number": 1,
        "question": "What is database normalization?",
        "marks": 5,
    },
    {
        "question_number": 2,
        "question": "Explain Second Normal Form (2NF).",
        "marks": 10,
    },
    {
        "question_number": 3,
        "question": "Explain the difference between 2NF and 3NF.",
        "marks": 10,
    },
]
# ============================================================
# QUESTION AREA
# ============================================================
# ============================================================
# QUESTION BANK
# ============================================================

# ============================================================
# QUESTION BANK
# ============================================================

selected_question = render_question_bank(mock_questions)

if selected_question:

    st.session_state["selected_question"] = selected_question

    if not uploaded_file:

        st.warning(
            "Please upload an academic document first."
        )

    else:

        temp_file_path = None

        try:

            # --------------------------------------------
            # PROCESS UPLOADED DOCUMENT
            # --------------------------------------------

            with st.spinner(
                "Processing your academic material..."
            ):

                suffix = Path(uploaded_file.name).suffix

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=suffix,
                ) as temp_file:

                    temp_file.write(
                        uploaded_file.getbuffer()
                    )

                    temp_file_path = temp_file.name

                document_result = process_document(
                    temp_file_path
                )

            # --------------------------------------------
            # CHECK DOCUMENT
            # --------------------------------------------

            if "error" in document_result:

                st.error(
                    document_result["error"]
                )

            else:

                document_text = document_result["text"]

                st.session_state["document_text"] = document_text

                if not document_text.strip():

                    st.error(
                        "No readable text could be extracted "
                        "from the uploaded document."
                    )

                else:

                    # ----------------------------------------
                    # GENERATE SOLUTION
                    # ----------------------------------------

                    with st.spinner(
                        "Generating solution..."
                    ):

                        answer, sources = generate_answer(
                            selected_question["question"],
                            document_text,
                        )

        except Exception as e:

            st.error(
                "Something went wrong while generating "
                "the solution."
            )

            st.exception(e)

        finally:

            if (
                temp_file_path
                and os.path.exists(temp_file_path)
            ):
                os.remove(temp_file_path)

st.markdown(
    '<div class="section-title">❓ Ask a Question</div>',
    unsafe_allow_html=True,
)

question = st.text_area(
    "What would you like to understand?",
    placeholder=(
        "Example: Explain Second Normal Form "
        "with a simple example."
    ),
    height=140,
    label_visibility="visible",
)

ask_button = st.button(
    "🔍 Ask AI",
    type="primary",
)


# ============================================================
# ANSWER + SOURCES
# ============================================================




if ask_button:

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not uploaded_file:
        st.warning(
            "Please upload an academic document first."
        )

    elif not question.strip():
        st.warning(
            "Please enter a question."
        )

    else:

        temp_file_path = None

        try:

            # ------------------------------------------------
            # STEP 1 — SAVE UPLOADED FILE TEMPORARILY
            # ------------------------------------------------

            with st.spinner(
                "Processing your academic material..."
            ):

                suffix = Path(uploaded_file.name).suffix

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=suffix,
                ) as temp_file:

                    temp_file.write(
                        uploaded_file.getbuffer()
                    )

                    temp_file_path = temp_file.name

                # --------------------------------------------
                # STEP 2 — MEMBER 2 DOCUMENT PROCESSOR
                # --------------------------------------------

                document_result = process_document(
                    temp_file_path
                )

            # ------------------------------------------------
            # STEP 3 — CHECK PROCESSING RESULT
            # ------------------------------------------------

            if "error" in document_result:

                st.error(
                    document_result["error"]
                )

            else:

                document_text = document_result["text"]

                st.session_state["document_text"] = document_text

                if not document_text.strip():

                    st.error(
                        "No readable text could be extracted "
                        "from the uploaded document."
                    )

                else:

                    # ----------------------------------------
                    # DOCUMENT INFORMATION
                    # ----------------------------------------

                    st.success(
                        f"Document processed successfully "
                        f"({document_result['category']})."
                    )

                    # ----------------------------------------
                    # STEP 4 — MEMBER 1 RAG PIPELINE
                    # ----------------------------------------

                    with st.spinner(
                        "Generating your answer..."
                    ):

                        answer, sources = generate_answer(
                            question.strip(),
                            document_text,
                        )

        except Exception as e:

            st.error(
                "Something went wrong while processing "
                "your document or generating the answer."
            )

            st.exception(e)

        finally:

            # ----------------------------------------------
            # STEP 5 — DELETE TEMPORARY FILE
            # ----------------------------------------------

            if (
                temp_file_path
                and os.path.exists(temp_file_path)
            ):
                os.remove(temp_file_path)


# ============================================================
# DISPLAY ANSWER
# ============================================================

if answer:

    render_answer(
        answer=answer
    )

else:

    render_answer()


# ============================================================
# DISPLAY SOURCES
# ============================================================

render_sources(
    sources
)
