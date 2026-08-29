import os
import sys
import tempfile
from pathlib import Path

# ============================================================
# PROJECT PATH
# ============================================================

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
from document_processing.question_extractor import extract_questions

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


# ============================================================
# SESSION STATE
# ============================================================

if "document_text" not in st.session_state:
    st.session_state["document_text"] = ""

if "questions" not in st.session_state:
    st.session_state["questions"] = []

if "processed_filename" not in st.session_state:
    st.session_state["processed_filename"] = None

if "document_category" not in st.session_state:
    st.session_state["document_category"] = None

if "document_metadata" not in st.session_state:
    st.session_state["document_metadata"] = {}

if "content_units" not in st.session_state:
    st.session_state["content_units"] = []

if "selected_question" not in st.session_state:
    st.session_state["selected_question"] = None


# ============================================================
# PROCESS UPLOADED DOCUMENT
# ============================================================

if uploaded_file:

    # Process only when a new/different document is uploaded.
    if (
        st.session_state["processed_filename"]
        != uploaded_file.name
    ):

        temp_file_path = None

        try:

            with st.spinner(
                "Processing your academic material..."
            ):

                # ------------------------------------------------
                # SAVE UPLOADED FILE TEMPORARILY
                # ------------------------------------------------

                suffix = Path(
                    uploaded_file.name
                ).suffix

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=suffix,
                ) as temp_file:

                    temp_file.write(
                        uploaded_file.getbuffer()
                    )

                    temp_file_path = temp_file.name

                # ------------------------------------------------
                # PROCESS DOCUMENT
                # ------------------------------------------------

                document_result = process_document(
                    temp_file_path,
                    uploaded_file.name,
                    subject=subject,
                    topic=topic,
                )

            # ----------------------------------------------------
            # HANDLE PROCESSING ERROR
            # ----------------------------------------------------

            if "error" in document_result:

                st.error(
                    document_result["error"]
                )

                st.session_state["document_text"] = ""
                st.session_state["questions"] = []
                st.session_state["document_category"] = None
                st.session_state["document_metadata"] = {}
                st.session_state["content_units"] = []
                st.session_state["selected_question"] = None

            else:

                document_text = document_result.get(
                    "text",
                    "",
                )

                # ------------------------------------------------
                # CHECK EXTRACTED TEXT
                # ------------------------------------------------

                if not document_text.strip():

                    st.error(
                        "No readable text could be extracted "
                        "from the uploaded document."
                    )

                    st.session_state["document_text"] = ""
                    st.session_state["questions"] = []
                    st.session_state["document_category"] = None
                    st.session_state["document_metadata"] = {}
                    st.session_state["content_units"] = []
                    st.session_state["selected_question"] = None

                else:

                    # ------------------------------------------------
                    # STORE DOCUMENT INFORMATION
                    # ------------------------------------------------

                    st.session_state["document_text"] = (
                        document_text
                    )

                    st.session_state["document_category"] = (
                        document_result.get(
                            "category",
                            "General",
                        )
                    )

                    st.session_state["document_metadata"] = (
                        document_result.get(
                            "metadata",
                            {},
                        )
                    )

                    st.session_state["content_units"] = (
                        document_result.get(
                            "content_units",
                            [],
                        )
                    )

                    # ------------------------------------------------
                    # EXTRACT QUESTIONS
                    # ------------------------------------------------

                    questions = extract_questions(
                        document_text
                    )

                    st.session_state["questions"] = (
                        questions
                    )

                    st.session_state["processed_filename"] = (
                        uploaded_file.name
                    )

                    st.session_state["selected_question"] = None

                    st.success(
                        f"Document processed successfully "
                        f"({document_result.get('category', 'General')})."
                    )

        except Exception as e:

            st.error(
                "Something went wrong while processing "
                "the document."
            )

            st.exception(e)

            # Clear invalid document state.
            st.session_state["document_text"] = ""
            st.session_state["questions"] = []
            st.session_state["document_category"] = None
            st.session_state["document_metadata"] = {}
            st.session_state["content_units"] = []
            st.session_state["selected_question"] = None

        finally:

            # ------------------------------------------------
            # DELETE TEMPORARY FILE
            # ------------------------------------------------

            if (
                temp_file_path
                and os.path.exists(temp_file_path)
            ):

                os.remove(
                    temp_file_path
                )

else:

    # ========================================================
    # CLEAR OLD DOCUMENT DATA
    # ========================================================

    st.session_state["document_text"] = ""
    st.session_state["questions"] = []
    st.session_state["processed_filename"] = None
    st.session_state["document_category"] = None
    st.session_state["document_metadata"] = {}
    st.session_state["content_units"] = []
    st.session_state["selected_question"] = None


# ============================================================
# QUESTION BANK
# ============================================================

questions = st.session_state.get(
    "questions",
    []
)

selected_question = render_question_bank(
    questions
)

if selected_question:

    st.session_state["selected_question"] = (
        selected_question
    )

    # --------------------------------------------------------
    # GENERATE SOLUTION FOR SELECTED QUESTION
    # --------------------------------------------------------

    document_text = st.session_state.get(
        "document_text",
        "",
    )

    if document_text:

        with st.spinner(
            "Generating solution..."
        ):

            answer, sources = generate_answer(
                question=selected_question["question"],
                document_text=document_text,
                question_type=selected_question.get(
                    "type",
                    "theory",
                ),
                options=selected_question.get(
                    "options",
                    {},
                ),
                marks=selected_question.get(
                    "marks",
                ),
                document_metadata=st.session_state.get(
                    "document_metadata",
                    {},
                ),
                content_units=st.session_state.get(
                    "content_units",
                    [],
                ),
            )

        st.markdown(
            '<div class="section-title">'
            "🤖 Generated Solution"
            "</div>",
            unsafe_allow_html=True,
        )

        render_answer(
            answer=answer
        )

        render_sources(
            sources
        )


# ============================================================
# ASK A QUESTION
# ============================================================

st.markdown(
    '<div class="section-title">'
    "❓ Ask a Question"
    "</div>",
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
# MANUAL QUESTION → RAG
# ============================================================

if ask_button:

    if not uploaded_file:

        st.warning(
            "Please upload an academic document first."
        )

    elif not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        document_text = st.session_state.get(
            "document_text",
            "",
        )

        if not document_text:

            st.error(
                "The uploaded document could not be processed."
            )

        else:

            try:

                with st.spinner(
                    "Generating your answer..."
                ):

                    answer, sources = generate_answer(
                        question=question.strip(),
                        document_text=document_text,
                        document_metadata=st.session_state.get(
                            "document_metadata",
                            {},
                        ),
                        content_units=st.session_state.get(
                            "content_units",
                            [],
                        ),
                    )

                # --------------------------------------------
                # ANSWER
                # --------------------------------------------

                render_answer(
                    answer=answer
                )

                # --------------------------------------------
                # SOURCES
                # --------------------------------------------

                render_sources(
                    sources
                )

            except Exception as e:

                st.error(
                    "Something went wrong while generating "
                    "the answer."
                )

                st.exception(e)


# ============================================================
# DEFAULT ANSWER AREA
# ============================================================

elif not selected_question:

    render_answer()