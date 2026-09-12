import streamlit as st


def render_sidebar():
    """Render the document and programming learning configuration sidebar."""

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
        # LEARNING DETAILS
        # ----------------------------------------------------

        st.header("📖 Learning Details")

        subject = st.text_input(
            "Subject",
            placeholder="e.g. Data Structures",
        )

        programming_language = st.selectbox(
            "Programming Language",
            [
                "Python",
                "C",
                "C++",
                "Java",
                "JavaScript",
                "Other",
            ],
            index=None,
            placeholder="Select a programming language",
        )

        chapter = st.text_input(
            "Chapter",
            placeholder="e.g. Searching Algorithms",
        )

        topic = st.text_input(
            "Topic",
            placeholder="e.g. Binary Search",
        )

        st.divider()

        # ----------------------------------------------------
        # LEARNING FLOW
        # ----------------------------------------------------

        st.subheader("🎓 Learning Path")

        st.markdown(
            f"""
            **Subject**

            {subject if subject else "Not selected"}

            ↓

            **Language**

            {
                programming_language
                if programming_language
                else "Not selected"
            }

            ↓

            **Chapter**

            {chapter if chapter else "Not selected"}

            ↓

            **Topic**

            {topic if topic else "Not selected"}
            """
        )

        st.divider()

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        st.subheader("⚡ Status")

        if uploaded_file:
            st.success("Document ready for learning.")
        else:
            st.warning("Waiting for a document.")

    return (
        uploaded_file,
        subject,
        programming_language,
        chapter,
        topic,
    )