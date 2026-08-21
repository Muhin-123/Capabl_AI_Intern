import streamlit as st


def render_sources(sources=None):
    """Display sources retrieved by the RAG pipeline."""

    st.header("📚 Retrieved Sources")

    if not sources:
        st.caption(
            "Relevant document sources will appear here "
            "after the RAG pipeline is connected."
        )
        return

    for index, source in enumerate(sources, start=1):

        with st.expander(f"Source {index}"):

            if hasattr(source, "page_content"):
                st.write(source.page_content)
            else:
                st.write(source)