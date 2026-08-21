from PyPDF2 import PdfReader
from docx import Document
from pptx import Presentation


def extract_pdf(file_path):
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


def extract_docx(file_path):
    document = Document(file_path)

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text


def extract_pptx(file_path):
    presentation = Presentation(file_path)

    text = ""

    for slide in presentation.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text += shape.text + "\n"

    return text


def clean_text(text):
    text = " ".join(text.split())
    return text.strip()


def categorize_document(file_path):
    filename = file_path.lower()

    if "question" in filename or "qp" in filename:
        return "questions"

    elif "lab" in filename or "manual" in filename:
        return "lab"

    elif "textbook" in filename or "book" in filename:
        return "textbook"

    elif "note" in filename or "lecture" in filename:
        return "notes"

    else:
        return "general"


def process_document(file_path):

    if file_path.lower().endswith(".pdf"):
        text = extract_pdf(file_path)

    elif file_path.lower().endswith(".docx"):
        text = extract_docx(file_path)

    elif file_path.lower().endswith(".pptx"):
        text = extract_pptx(file_path)

    else:
        return {
            "error": "Unsupported file type"
        }

    text = clean_text(text)
    category = categorize_document(file_path)

    return {
        "filename": file_path,
        "category": category,
        "text": text
    }