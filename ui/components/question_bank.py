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

    # --------------------------------------------------------
    # QUESTION LABELS
    # --------------------------------------------------------

    question_labels = [
        f"{q['section']} - Q{q['question_number']}"
        for q in questions
    ]

    # --------------------------------------------------------
    # QUESTION SELECTION
    # --------------------------------------------------------

    selected_label = st.selectbox(
        "Select a question",
        question_labels,
    )

    selected_question = next(
        q
        for q in questions
        if (
            f"{q['section']} - Q{q['question_number']}"
            == selected_label
        )
    )

    # --------------------------------------------------------
    # QUESTION
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Question</div>',
        unsafe_allow_html=True,
    )

    st.write(
        selected_question["question"]
    )

    # --------------------------------------------------------
    # MARKS
    # --------------------------------------------------------

    st.caption(
        f"Marks: {selected_question['marks']}"
    )

    # --------------------------------------------------------
    # OPTIONS
    # --------------------------------------------------------

    options = selected_question.get(
        "options",
        {}
    )

    if options:

        st.markdown("**Options:**")

        for letter, option_text in options.items():

            st.write(
                f"**{letter}.** {option_text}"
            )

    # --------------------------------------------------------
    # QUESTION TYPE
    # --------------------------------------------------------

    question_type = selected_question.get(
        "type",
        "unknown",
    )

    if question_type == "multiple_select":

        st.caption(
            "Question type: Multiple Select"
        )

    elif question_type == "numerical":

        st.caption(
            "Question type: Numerical Answer"
        )

    elif question_type == "mcq":

        st.caption(
            "Question type: Multiple Choice"
        )

    # --------------------------------------------------------
    # GENERATE SOLUTION
    # --------------------------------------------------------

    generate_button = st.button(
        "🧠 Generate Solution",
        key=f"generate_{selected_question['id']}",
        type="primary",
    )

    if generate_button:
        return selected_question

    return None