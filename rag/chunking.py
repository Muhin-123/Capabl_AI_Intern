from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text(text: str):
    """Split extracted document text into smaller chunks."""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )

    return splitter.split_text(text)