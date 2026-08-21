import streamlit as st


def render_sidebar():
    """Render the document and academic details sidebar."""

    with st.sidebar:

        # ----------------------------------------------------
        # DOCUMENT
        # ----------------------------------------------------

        st.header("📚 Document")

        uploaded_file = st.file_uploader(
            "Upload your academic material",
            type=["pdf", "docx", "pptx"],
            help="Supported formats: PDF, DOCX, and PPTX.",
        )

        if uploaded_file:
            st.success("✓ Document ready")

            st.markdown(
                f"""
                **📄 File**

                `{uploaded_file.name}`
                """
            )
        else:
            st.info(
                "Upload a PDF, DOCX, or PPTX "
                "to get started."
            )

        st.divider()

        # ----------------------------------------------------
        # ACADEMIC DETAILS
        # ----------------------------------------------------

        st.header("📖 Academic Details")

        subject = st.text_input(
            "Subject",
            placeholder="e.g. Database Systems",
        )

        topic = st.text_input(
            "Topic",
            placeholder="e.g. Normalization",
        )

        st.divider()

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        st.subheader("⚡ Status")

        if uploaded_file:
            st.success("Document ready for questions.")
        else:
            st.warning("Waiting for a document.")

    return uploaded_file, subject, topic