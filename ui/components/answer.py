import streamlit as st


def render_answer(answer=None, loading=False):
    """Display the AI-generated answer."""

    st.header("🤖 AI Answer")

    if loading:
        with st.spinner("Analyzing your academic material..."):
            st.write("Generating answer...")
        return

    if answer:
        st.markdown(answer)
    else:
        st.caption(
            "Your AI-generated answer will appear here."
        )