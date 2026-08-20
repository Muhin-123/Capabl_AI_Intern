import streamlit as st


def render_sidebar():
    """Render the document and academic details sidebar."""

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

    return uploaded_file, subject, topic