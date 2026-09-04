import streamlit as st

from rag.pipeline import generate_learning_content


def render_learning_interface(
    subject=None,
    chapter=None,
    topic=None,
    document_text=None,
    document_metadata=None,
    content_units=None,
):
    """Render the Week 3 topic-based learning interface."""

    st.markdown(
        '<div class="section-title">🎓 Learn a Topic</div>',
        unsafe_allow_html=True,
    )

    # ----------------------------------------------------
    # LEARNING PATH
    # ----------------------------------------------------

    if subject:
        st.caption(f"📖 Subject: {subject}")

    if chapter:
        st.caption(f"📚 Chapter: {chapter}")

    if topic:
        st.caption(f"🎯 Topic: {topic}")

    st.divider()

    # ----------------------------------------------------
    # VALIDATION
    # ----------------------------------------------------

    if not document_text:
        st.info(
            "Upload an academic document to start learning."
        )
        return None

    if not subject:
        st.info(
            "Enter a subject in the sidebar to start learning."
        )
        return None

    if not chapter:
        st.info(
            "Enter a chapter in the sidebar to continue."
        )
        return None

    if not topic:
        st.info(
            "Enter a topic in the sidebar to continue."
        )
        return None

    # ----------------------------------------------------
    # LEARN BUTTON
    # ----------------------------------------------------

    learn_button = st.button(
        "🚀 Learn This Topic",
        type="primary",
        use_container_width=True,
    )

    if not learn_button:
        return None

    # ----------------------------------------------------
    # GENERATE LEARNING CONTENT
    # ----------------------------------------------------

    with st.spinner(
        "🧠 Generating your learning material..."
    ):

        try:

            learning_content, sources = (
                generate_learning_content(
                    subject=subject,
                    chapter=chapter,
                    topic=topic,
                    document_text=document_text,
                    document_metadata=document_metadata,
                    content_units=content_units,
                )
            )

        except Exception as e:

            st.error(
                f"Unable to generate learning content: {e}"
            )

            return None

    # ----------------------------------------------------
    # EXPLANATION
    # ----------------------------------------------------

    st.markdown("### 📘 Explanation")

    explanation = learning_content.get(
        "explanation"
    )

    if explanation:
        st.write(explanation)
    else:
        st.info(
            "No explanation was generated."
        )

    # ----------------------------------------------------
    # EXAMPLE
    # ----------------------------------------------------

    st.markdown("### 💡 Example")

    example = learning_content.get(
        "example"
    )

    if example:
        st.write(example)
    else:
        st.info(
            "No example was generated."
        )

    # ----------------------------------------------------
    # PRACTICE QUESTION
    # ----------------------------------------------------

    st.markdown("### 📝 Practice Question")

    practice_question = learning_content.get(
        "practice_question"
    )

    if practice_question:
        st.write(practice_question)
    else:
        st.info(
            "No practice question was generated."
        )

    # ----------------------------------------------------
    # LEARNING SOURCES
    # ----------------------------------------------------

    if sources:
        st.markdown("### 🔎 Learning Sources")

        for i, source in enumerate(sources, start=1):

            metadata = getattr(
                source,
                "metadata",
                {},
            )

            filename = metadata.get(
                "filename",
                metadata.get(
                    "source",
                    "Unknown file",
                ),
            )

            file_type = metadata.get(
                "file_type",
                "",
            )

            page = metadata.get(
                "page",
            )

            slide = metadata.get(
                "slide",
            )

            st.markdown(
                f"**Source {i}**"
            )

            st.caption(
                f"📄 {filename}"
            )

            if file_type:
                st.caption(
                    f"📁 Type: {file_type}"
                )

            if page is not None:
                st.caption(
                    f"📖 Page: {page}"
                )

            if slide is not None:
                st.caption(
                    f"📊 Slide: {slide}"
                )

            with st.expander("View source content"):
                st.write(
                    source.page_content
                )

    # ----------------------------------------------------
    # RETURN RESULT
    # ----------------------------------------------------

    return {
        "subject": subject,
        "chapter": chapter,
        "topic": topic,
        "learning_content": learning_content,
        "sources": sources,
    }
