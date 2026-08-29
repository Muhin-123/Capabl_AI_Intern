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

    if "question" in filename or "qp" in filename or "question bank" in filename:
        return "Question Paper"

    elif "lab" in filename or "manual" in filename:
        return "Lab Manual"

    elif "textbook" in filename or "book" in filename:
        return "Textbook"

    elif "note" in filename or "lecture" in filename:
        return "Notes"

    else:
        return "General"


def detect_document_type(file_path):
    filename = file_path.lower()

    if filename.endswith(".pdf"):
        return "PDF"

    elif filename.endswith(".docx"):
        return "DOCX"

    elif filename.endswith(".pptx"):
        return "PPTX"

    else:
        return "Unsupported"
def process_document(file_path):

    try:
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

        if not text:
            return {
                "filename": file_path,
                "file_type": detect_document_type(file_path),
                "category": "Unknown",
                "text": "",
                "error": "The document is empty or contains no readable text"
            }

        category = categorize_document(file_path)

        return {
            "filename": file_path,
            "file_type": detect_document_type(file_path),
            "category": category,
            "text": text
        }

    except Exception as e:
        return {
            "filename": file_path,
            "file_type": detect_document_type(file_path),
            "category": "Unknown",
            "text": "",
            "error": "The document could not be processed"
        }
result = process_document("../samples/Question Bank for Comprehensive Engineering Aptitude Test.pdf")

print("Filename:", result["filename"])
print("File Type:", result["file_type"])
print("Category:", result["category"])
print("Text:")
print(result["text"])
