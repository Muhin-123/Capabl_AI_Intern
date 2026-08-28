import streamlit as st


def render_question_bank(questions=None):
    """Render the Question Bank interface."""

    st.markdown(
        '<div class="section-title">📋 Question Bank</div>',
        unsafe_allow_html=True,
    )

    if not questions:
        st.info(
            "No questions have been extracted from this document yet."
        )
        return None

    question_labels = [
        f"Question {q['question_number']}"
        for q in questions
    ]

    selected_label = st.selectbox(
        "Select a question",
        question_labels,
    )

    selected_question = next(
        q
        for q in questions
        if f"Question {q['question_number']}" == selected_label
    )

    st.markdown("### Question")

    st.write(selected_question["question"])

    if selected_question.get("marks"):
        st.caption(
            f"Marks: {selected_question['marks']}"
        )

    generate_button = st.button(
        "🧠 Generate Solution",
        type="primary",
    )

    if generate_button:
        return selected_question

    return None