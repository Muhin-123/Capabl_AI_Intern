import streamlit as st

from rag.pipeline import generate_learning_content


def render_learning_interface(
    subject=None,
    programming_language=None,
    chapter=None,
    topic=None,
    document_text=None,
    document_metadata=None,
    content_units=None,
):
    """Render the Week 5 programming-focused learning interface."""

    st.markdown(
        '<div class="section-title">💻 Programming Learning</div>',
        unsafe_allow_html=True,
    )

    # ----------------------------------------------------
    # LEARNING PATH
    # ----------------------------------------------------

    if subject:
        st.caption(f"📖 Subject: {subject}")

    if programming_language:
        st.caption(
            f"💻 Programming Language: "
            f"{programming_language}"
        )

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

    if not programming_language:
        st.info(
            "Select a programming language in the sidebar."
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
    # PROGRAMMING QUESTION
    # ----------------------------------------------------

    st.markdown("### 🧑‍💻 Programming Question")

    programming_question = st.text_area(
    "What programming problem would you like to understand?",
    placeholder=(
        "Example: Explain binary search and "
        "show a Python implementation."
    ),
    height=140,
    help=(
        "Ask about an algorithm, data structure, "
        "programming concept, or coding problem."
    ),
)

    # ----------------------------------------------------
    # GENERATE BUTTON
    # ----------------------------------------------------

    generate_button = st.button(
        "🚀 Generate Programming Solution",
        type="primary",
        use_container_width=True,
    )

    if not generate_button:
        return None

    if not programming_question.strip():
        st.warning(
            "Please enter a programming question."
        )
        return None

    # ----------------------------------------------------
    # GENERATE LEARNING CONTENT
    # ----------------------------------------------------

    with st.spinner(
        "🧠 Generating your programming solution..."
    ):

        try:

            learning_content, sources = (
                generate_learning_content(
                    subject=subject,
                    programming_language=programming_language,
                    chapter=chapter,
                    topic=topic,
                    programming_question=programming_question,
                    document_text=document_text,
                    document_metadata=document_metadata,
                    content_units=content_units,
                 )
            )

        except Exception as e:

            st.error(
                "Unable to generate programming content."
            )

            st.exception(e)

            return None
    st.success("✅ Programming solution generated successfully.")
# ----------------------------------------------------
# CODE
# ----------------------------------------------------

code = learning_content.get(
    "code",
    "",
)

st.markdown("### 💻 Code")

code_language = {
    "Python": "python",
    "C": "c",
    "C++": "cpp",
    "Java": "java",
    "JavaScript": "javascript",
}.get(programming_language, "text")

if code:
    st.code(
        code,
        language=code_language,
    )
else:
    st.info(
        "Code will appear here when the programming "
        "solution is generated."
    )

    # ----------------------------------------------------
    # EXPLANATION
    # ----------------------------------------------------

    st.markdown("### 🤖 Explanation")

    explanation = learning_content.get(
        "explanation",
        "",
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

    example = learning_content.get(
        "example",
        "",
    )

    if example:

        st.markdown("### 💡 Example")

        st.write(example)

    # ----------------------------------------------------
    # PRACTICE QUESTION
    # ----------------------------------------------------

    st.markdown("### 📝 Practice Question")

    practice_question = learning_content.get(
        "practice_question",
        "",
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

        for i, source in enumerate(
            sources,
            start=1,
        ):

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

            with st.expander(
                "View source content"
            ):
                st.write(
                    source.page_content
                )

    # ----------------------------------------------------
    # RETURN RESULT
    # ----------------------------------------------------

    return {
        "subject": subject,
        "programming_language": programming_language,
        "chapter": chapter,
        "topic": topic,
        "question": programming_question,
        "learning_content": learning_content,
        "sources": sources,
    }