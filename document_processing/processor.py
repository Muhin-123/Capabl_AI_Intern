from PyPDF2 import PdfReader
from docx import Document
from pptx import Presentation
import os
import re

from classifier import classify_document


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
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def categorize_document(file_path, text=""):
    filename = os.path.basename(file_path).lower()
    content = text.lower()

    if (
        "question bank" in filename
        or "question paper" in filename
        or "exam paper" in filename
        or re.search(r"\bqb\b", filename)
        or "question bank" in content
    ):
        return "Question Paper"

    elif "lab manual" in filename or "practical manual" in filename:
        return "Lab Manual"

    elif "textbook" in filename or "text book" in filename:
        return "Textbook"

    elif "assignment" in filename:
        return "Assignment"

    elif "notes" in filename or "unit-" in filename or "lecture" in filename:
        return "Notes"

    return "General"

def detect_document_type(file_path):
    filename = file_path.lower()

    if filename.endswith(".pdf"):
        return "PDF"

    elif filename.endswith(".docx"):
        return "DOCX"

    elif filename.endswith(".pptx"):
        return "PPTX"

    return "Unsupported"


PROGRAMMING_LANGUAGE_KEYWORDS = {
    "Python": [
        "python programming",
        "python program",
        "python language",
        "def ",
        "import numpy",
        "import pandas",
        "pip install",
        "print("
    ],

    "C": [
        "c programming",
        "c program",
        "#include <stdio.h>",
        "printf(",
        "scanf(",
        "malloc("
    ],

    "C++": [
        "c++ programming",
        "c++ program",
        "#include <iostream>",
        "using namespace std",
        "cout <<",
        "cin >>"
    ],

    "Java": [
        "java programming",
        "java program",
        "java language",
        "public static void main",
        "system.out.println"
    ],

    "JavaScript": [
        "javascript programming",
        "javascript program",
        "console.log(",
        "function("
    ],

    "SQL": [
        "sql query",
        "structured query language",
        "select * from",
        "insert into",
        "update ",
        "delete from",
        "create table"
    ]
}


def classify_programming_language(file_path, text=""):
    content = f"{file_path} {text}".lower()

    language_scores = {}

    for language, keywords in PROGRAMMING_LANGUAGE_KEYWORDS.items():

        score = 0

        for keyword in keywords:
            if keyword.lower() in content:
                score += 1

        if score > 0:
            language_scores[language] = score

    if not language_scores:
        return "None"

    best_language = max(
        language_scores,
        key=language_scores.get
    )

    # Require stronger evidence before identifying a language.
    if language_scores[best_language] < 2:
        return "None"

    return best_language


def classify_content_type(text):
    content = text.lower()

    content_types = []

    code_keywords = [
        "def ",
        "import ",
        "#include",
        "printf(",
        "scanf(",
        "public static void main",
        "select ",
        "insert into",
        "create table",
        "for(",
        "while(",
        "if(",
        "class "
    ]

    example_keywords = [
        "example",
        "for example",
        "sample program",
        "sample code",
        "illustration",
        "consider the following"
    ]

    technical_keywords = [
        "algorithm",
        "architecture",
        "protocol",
        "database",
        "network",
        "operating system",
        "implementation",
        "methodology",
        "framework"
    ]

    if any(keyword in content for keyword in code_keywords):
        content_types.append("Code")

    if any(keyword in content for keyword in example_keywords):
        content_types.append("Example")

    if any(keyword in content for keyword in technical_keywords):
        content_types.append("Technical")

    if not content_types:
        content_types.append("Theory")

    return content_types


def process_document(
    file_path,
    original_filename=None,
    subject=None,
    topic=None
):

    classification_name = (
        original_filename
        or os.path.basename(file_path)
    )

    try:

        if file_path.lower().endswith(".pdf"):
            text = extract_pdf(file_path)

        elif file_path.lower().endswith(".docx"):
            text = extract_docx(file_path)

        elif file_path.lower().endswith(".pptx"):
            text = extract_pptx(file_path)

        else:
            return {
                "filename": classification_name,
                "file_type": "Unsupported",
                "category": "Unknown",
                "subject": "Unknown",
                "chapter": "Unknown",
                "topic": "Unknown",
                "chapters": [],
                "topics": [],
                "programming_language": "None",
                "content_type": [],
                "text": "",
                "error": "Unsupported file type"
            }

        text = clean_text(text)

        if not text:
            return {
                "filename": classification_name,
                "file_type": detect_document_type(file_path),
                "category": "Unknown",
                "subject": "Unknown",
                "chapter": "Unknown",
                "topic": "Unknown",
                "chapters": [],
                "topics": [],
                "programming_language": "None",
                "content_type": [],
                "text": "",
                "error": "The document is empty or contains no readable text"
            }

        category = categorize_document(
            classification_name,
            text
        )

        classification = classify_document(
            classification_name,
            text
        )

        detected_subject = classification["subject"]
        detected_chapter = classification["chapter"]
        detected_topic = classification["topic"]

        final_subject = subject if subject else detected_subject
        final_topic = topic if topic else detected_topic

        programming_language = classify_programming_language(
            classification_name,
            text
        )

        content_type = classify_content_type(text)

        return {
            "filename": classification_name,
            "file_type": detect_document_type(file_path),
            "category": category,
            "subject": final_subject,
            "chapter": detected_chapter,
            "topic": final_topic,
            "chapters": classification["chapters"],
            "topics": classification["topics"],
            "programming_language": programming_language,
            "content_type": content_type,
            "text": text
        }

    except Exception:
        return {
            "filename": classification_name,
            "file_type": detect_document_type(file_path),
            "category": "Unknown",
            "subject": "Unknown",
            "chapter": "Unknown",
            "topic": "Unknown",
            "chapters": [],
            "topics": [],
            "programming_language": "None",
            "content_type": [],
            "text": "",
            "error": "The document could not be processed"
        }