import streamlit as st


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

with st.sidebar:
    st.header("📚 Document")

    uploaded_file = st.file_uploader(
        "Upload academic material",
        type=["pdf", "docx", "pptx"],
    )

    if uploaded_file:
        st.success("Document uploaded")
        st.caption(f"**File:** {uploaded_file.name}")

    st.divider()

    st.subheader("📖 Academic Details")

    subject = st.text_input(
        "Subject",
        placeholder="e.g. Database Management Systems",
    )

    topic = st.text_input(
        "Topic",
        placeholder="e.g. Normalization",
    )

    st.divider()

    if uploaded_file:
        st.info("Document ready for processing.")
    else:
        st.warning("Please upload a document.")


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

st.header("🤖 AI Answer")

if ask_button:

    if not uploaded_file:
        st.warning("Please upload an academic document first.")

    elif not question.strip():
        st.warning("Please enter a question.")

    else:
        with st.spinner("Analyzing your academic material..."):
            st.info(
                "RAG backend integration will be connected here."
            )

else:
    st.caption(
        "Your AI-generated answer will appear here."
    )


# ============================================================
# SOURCES
# ============================================================

st.header("📖 Retrieved Sources")

st.caption(
    "Relevant document sources will appear here "
    "after the RAG pipeline is connected."
)