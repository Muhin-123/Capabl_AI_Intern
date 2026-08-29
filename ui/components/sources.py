import streamlit as st


def render_sources(sources=None):
    """Display sources retrieved by the RAG pipeline."""

    st.header("📚 Retrieved Sources")

    if not sources:
        st.caption(
            "No relevant document sources were retrieved."
        )
        return

    for index, source in enumerate(
        sources,
        start=1,
    ):

        with st.expander(
            f"Source {index}"
        ):

            # ------------------------------------------------
            # SOURCE CONTENT
            # ------------------------------------------------

            if hasattr(source, "page_content"):

                st.write(
                    source.page_content
                )

            else:

                st.write(source)

            # ------------------------------------------------
            # SOURCE METADATA
            # ------------------------------------------------

            metadata = getattr(
                source,
                "metadata",
                {},
            )

            if not metadata:
                continue

            st.divider()

            st.markdown(
                "**Source Information**"
            )

            filename = metadata.get(
                "filename"
            ) or metadata.get(
                "source"
            )

            if filename:
                st.caption(
                    f"📄 File: {filename}"
                )

            file_type = metadata.get(
                "file_type"
            )

            if file_type:
                st.caption(
                    f"📁 Type: {file_type}"
                )

            page = metadata.get(
                "page"
            )

            if page is not None:
                st.caption(
                    f"📖 Page: {page}"
                )

            slide = metadata.get(
                "slide"
            )

            if slide is not None:
                st.caption(
                    f"📊 Slide: {slide}"
                )

            subject = metadata.get(
                "subject"
            )

            if subject:
                st.caption(
                    f"📚 Subject: {subject}"
                )

            topic = metadata.get(
                "topic"
            )

            if topic:
                st.caption(
                    f"📝 Topic: {topic}"
                )

            category = metadata.get(
                "category"
            )

            if category:
                st.caption(
                    f"🏷️ Category: {category}"
                )