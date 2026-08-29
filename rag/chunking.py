from langchain_core.documents import Document
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)


def split_text(
    text: str,
    metadata=None,
    content_units=None,
):
    """
    Split document text into chunks while preserving
    document metadata.

    If content_units are provided, each page/slide is
    chunked separately so its metadata is retained.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )

    documents = []

    # --------------------------------------------------------
    # PAGE / SLIDE AWARE CHUNKING
    # --------------------------------------------------------

    if content_units:

        for unit in content_units:

            unit_text = unit.get(
                "text",
                "",
            ).strip()

            if not unit_text:
                continue

            unit_metadata = dict(
                metadata or {}
            )

            # Add page number if available.
            if "page" in unit:
                unit_metadata["page"] = unit[
                    "page"
                ]

            # Add slide number if available.
            if "slide" in unit:
                unit_metadata["slide"] = unit[
                    "slide"
                ]

            chunks = splitter.split_text(
                unit_text
            )

            for chunk in chunks:

                documents.append(
                    Document(
                        page_content=chunk,
                        metadata=unit_metadata.copy(),
                    )
                )

        return documents

    # --------------------------------------------------------
    # FALLBACK — TEXT ONLY
    # --------------------------------------------------------

    chunks = splitter.split_text(
        text
    )

    base_metadata = dict(
        metadata or {}
    )

    for chunk in chunks:

        documents.append(
            Document(
                page_content=chunk,
                metadata=base_metadata.copy(),
            )
        )

    return documents