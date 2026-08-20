import streamlit as st

from components.sidebar import render_sidebar
from components.answer import render_answer
from components.sources import render_sources

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Academic AI Agent",
    page_icon="🎓",
    layout="wide",
)


# ============================================================
# HEADER
# ============================================================

st.title("🎓 Academic AI Agent")

st.write(
    "Upload your academic material and ask questions "
    "based on the content."
)

st.divider()

# ============================================================
# SIDEBAR — DOCUMENT SETTINGS
# ============================================================

uploaded_file, subject, topic = render_sidebar()


# ============================================================
# MAIN AREA — QUESTION
# ============================================================

st.header("❓ Ask a Question")

question = st.text_area(
    "Enter your question",
    placeholder=(
        "Example: Explain Second Normal Form "
        "with a simple example."
    ),
    height=130,
)


ask_button = st.button(
    "🔍 Ask AI",
    type="primary",
    use_container_width=False,
)


# ============================================================
# ANSWER
# ============================================================

if ask_button:

    if not uploaded_file:
        st.warning("Please upload an academic document first.")

    elif not question.strip():
        st.warning("Please enter a question.")

    else:
        render_answer(
            answer="RAG backend integration will be connected here."
        )

else:
    render_answer()


# ============================================================
# SOURCES
# ============================================================

render_sources()