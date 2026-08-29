from PyPDF2 import PdfReader
from docx import Document
from pptx import Presentation


# ============================================================
# PDF EXTRACTION
# ============================================================

def extract_pdf(file_path):
    """
    Extract PDF text while preserving page-level information.

    Returns:
        {
            "text": "...",
            "pages": [
                {
                    "text": "...",
                    "page": 1
                },
                ...
            ]
        }
    """

    reader = PdfReader(file_path)

    pages = []
    full_text = []

    for page_number, page in enumerate(
        reader.pages,
        start=1,
    ):
        page_text = page.extract_text() or ""

        if page_text.strip():
            pages.append(
                {
                    "text": page_text,
                    "page": page_number,
                }
            )

            full_text.append(page_text)

    return {
        "text": "\n".join(full_text),
        "pages": pages,
    }


# ============================================================
# DOCX EXTRACTION
# ============================================================

def extract_docx(file_path):
    """
    Extract DOCX text.

    DOCX files do not provide reliable page numbers through
    python-docx, so page is stored as None.
    """

    document = Document(file_path)

    paragraphs = []
    full_text = []

    for paragraph in document.paragraphs:

        paragraph_text = paragraph.text.strip()

        if paragraph_text:

            paragraphs.append(
                {
                    "text": paragraph_text,
                    "page": None,
                }
            )

            full_text.append(paragraph_text)

    return {
        "text": "\n".join(full_text),
        "pages": paragraphs,
    }


# ============================================================
# PPTX EXTRACTION
# ============================================================

def extract_pptx(file_path):
    """
    Extract PPTX text while preserving slide numbers.

    Returns:
        {
            "text": "...",
            "slides": [
                {
                    "text": "...",
                    "slide": 1
                },
                ...
            ]
        }
    """

    presentation = Presentation(file_path)

    slides = []
    full_text = []

    for slide_number, slide in enumerate(
        presentation.slides,
        start=1,
    ):

        slide_text = []

        for shape in slide.shapes:

            if hasattr(shape, "text"):

                shape_text = shape.text.strip()

                if shape_text:
                    slide_text.append(shape_text)

        combined_slide_text = "\n".join(
            slide_text
        )

        if combined_slide_text.strip():

            slides.append(
                {
                    "text": combined_slide_text,
                    "slide": slide_number,
                }
            )

            full_text.append(
                combined_slide_text
            )

    return {
        "text": "\n".join(full_text),
        "slides": slides,
    }


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text):
    """
    Clean extracted text while preserving readable content.
    """

    text = " ".join(text.split())

    return text.strip()


# ============================================================
# DOCUMENT CATEGORIZATION
# ============================================================

def categorize_document(file_path):
    """
    Categorize the document based on its filename.
    """

    filename = file_path.lower()

    if "question" in filename or "qp" in filename:
        return "Question Paper"

    elif "lab" in filename or "manual" in filename:
        return "Lab Manual"

    elif "textbook" in filename or "book" in filename:
        return "Textbook"

    elif "note" in filename or "lecture" in filename:
        return "Notes"

    else:
        return "General"


# ============================================================
# DOCUMENT TYPE
# ============================================================

def detect_document_type(file_path):
    """
    Detect the supported document type.
    """

    filename = file_path.lower()

    if filename.endswith(".pdf"):
        return "PDF"

    elif filename.endswith(".docx"):
        return "DOCX"

    elif filename.endswith(".pptx"):
        return "PPTX"

    else:
        return "Unsupported"


# ============================================================
# DOCUMENT PROCESSING
# ============================================================

def process_document(
    file_path,
    original_filename=None,
    subject=None,
    topic=None,
):
    """
    Process PDF, DOCX, or PPTX documents.

    The existing text-based output is preserved for
    backwards compatibility.

    Additional metadata is returned for RAG/source tracking.
    """

    try:

        file_type = detect_document_type(
            file_path
        )

        source = (
            original_filename
            or file_path
        )

        # ----------------------------------------------------
        # EXTRACT DOCUMENT
        # ----------------------------------------------------

        if file_type == "PDF":

            extracted = extract_pdf(
                file_path
            )

            text = extracted["text"]
            content_units = extracted["pages"]

        elif file_type == "DOCX":

            extracted = extract_docx(
                file_path
            )

            text = extracted["text"]
            content_units = extracted["pages"]

        elif file_type == "PPTX":

            extracted = extract_pptx(
                file_path
            )

            text = extracted["text"]
            content_units = extracted["slides"]

        else:

            return {
                "filename": source,
                "file_type": "Unsupported",
                "category": "Unknown",
                "text": "",
                "metadata": {},
                "content_units": [],
                "error": "Unsupported file type",
            }

        # ----------------------------------------------------
        # CLEAN FULL TEXT
        # ----------------------------------------------------

        text = clean_text(text)

        # ----------------------------------------------------
        # CHECK EMPTY DOCUMENT
        # ----------------------------------------------------

        if not text:

            return {
                "filename": source,
                "file_type": file_type,
                "category": "Unknown",
                "text": "",
                "metadata": {
                    "source": source,
                    "subject": subject,
                    "topic": topic,
                },
                "content_units": [],
                "error": (
                    "The document is empty or contains "
                    "no readable text"
                ),
            }

        # ----------------------------------------------------
        # CLEAN CONTENT UNITS
        # ----------------------------------------------------

        cleaned_units = []

        for unit in content_units:

            unit_text = clean_text(
                unit.get("text", "")
            )

            if not unit_text:
                continue

            cleaned_unit = {
                "text": unit_text,
            }

            if "page" in unit:
                cleaned_unit["page"] = unit[
                    "page"
                ]

            if "slide" in unit:
                cleaned_unit["slide"] = unit[
                    "slide"
                ]

            cleaned_units.append(
                cleaned_unit
            )

        # ----------------------------------------------------
        # CATEGORY
        # ----------------------------------------------------

        category = categorize_document(
            source
        )

        # ----------------------------------------------------
        # DOCUMENT METADATA
        # ----------------------------------------------------

        metadata = {
            "source": source,
            "filename": source,
            "file_type": file_type,
            "category": category,
            "subject": subject,
            "topic": topic,
        }

        # ----------------------------------------------------
        # RESULT
        # ----------------------------------------------------

        return {
            "filename": source,
            "file_type": file_type,
            "category": category,
            "text": text,
            "metadata": metadata,
            "content_units": cleaned_units,
        }

    except Exception:

        return {
            "filename": (
                original_filename
                or file_path
            ),
            "file_type": detect_document_type(
                file_path
            ),
            "category": "Unknown",
            "text": "",
            "metadata": {},
            "content_units": [],
            "error": (
                "The document could not be processed"
            ),
        }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    result = process_document(
        "../samples/DBMS_Lecture.pptx",
        original_filename="DBMS_Lecture.pptx",
        subject="DBMS",
        topic="Database Systems",
    )

    print(
        "Filename:",
        result["filename"],
    )

    print(
        "File Type:",
        result["file_type"],
    )

    print(
        "Category:",
        result["category"],
    )

    print(
        "Metadata:",
        result["metadata"],
    )

    print(
        "Content Units:",
        len(
            result["content_units"]
        ),
    )

    print(
        "Text:"
    )

    print(
        result["text"]
    )