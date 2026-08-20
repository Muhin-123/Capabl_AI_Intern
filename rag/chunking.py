from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_and_split_text(file_path: str):
    """Load a text file and split it into smaller chunks."""

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_text(text)

    return chunks


if __name__ == "__main__":
    chunks = load_and_split_text("data/sample.txt")

    print(f"Number of chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks, start=1):
        print(f"\n--- Chunk {i} ---")
        print(chunk)