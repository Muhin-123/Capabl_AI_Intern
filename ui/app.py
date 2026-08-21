import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from components.sidebar import render_sidebar
from components.answer import render_answer
from components.sources import render_sources
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
# QUESTION AREA
# ============================================================

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
# ANSWER AREA
# ============================================================

answer = None
sources = None

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
        try:
            with st.spinner(
                "Analyzing your academic material..."
            ):
                answer, sources = generate_answer(
                    question.strip()
                )

            render_answer(answer)

        except Exception as error:
            st.error(
                "Something went wrong while generating the answer."
            )

            st.exception(error)

else:
    render_answer()


# ============================================================
# SOURCES
# ============================================================

render_sources(sources)