# Academic AI Agent

## About

Academic AI Agent is an AI-based application that helps students
understand and solve questions from their academic documents.

Users can upload **PDF, DOCX, or PPTX** files and ask questions
about the content. The system processes the document, retrieves
relevant information using a RAG pipeline, and generates
AI-based answers with relevant sources.

For question papers, the system can also extract questions into
a structured **Question Bank** and generate solutions for the
extracted questions.

## Features

- Supports PDF, DOCX, and PPTX files
- Extracts and processes document content
- Automatically categorizes uploaded documents
- Retrieves relevant information using RAG
- Generates AI-based answers
- Displays retrieved sources
- Extracts questions from question papers
- Identifies question sections and types
- Displays question marks and options
- Supports Multiple Choice Questions (MCQ)
- Supports Multiple Select Questions
- Supports Numerical Answer Type Questions
- Generates solutions for extracted questions
- Provides step-by-step reasoning for numerical questions
- Simple Streamlit interface

## How It Works

### General Question Answering

1. Upload an academic document.
2. Enter the subject and topic.
3. Ask a question.
4. The system extracts the document content.
5. The document is split into smaller chunks.
6. Document chunks are converted into embeddings.
7. FAISS retrieves the most relevant information.
8. Google Gemini generates the answer.
9. Retrieved sources are displayed.

### Question Bank

1. Upload an academic question paper.
2. The system processes the document.
3. Question-paper sections are identified.
4. Questions are extracted and structured.
5. Question type, marks, and options are identified.
6. Extracted questions are displayed in the Question Bank.
7. Select a question.
8. Click **Generate Solution**.
9. The AI generates a solution based on the question and
   retrieved academic context.

## Technologies Used

- Python
- Streamlit
- LangChain
- FAISS
- Google Gemini
- Hugging Face Sentence Transformers
- PyPDF2
- python-docx
- python-pptx

## Project Structure

- **Document Processing** – Extracts and processes PDF, DOCX,
  and PPTX content.
- **Question Extraction** – Extracts and structures questions,
  question types, marks, and options from question papers.
- **Chunking** – Splits extracted document text into smaller
  chunks for retrieval.
- **Embeddings** – Converts document chunks into vector
  representations using Hugging Face embeddings.
- **Vector Store** – Stores and searches document embeddings
  using FAISS.
- **Retriever** – Retrieves the most relevant document chunks
  for a question.
- **RAG Pipeline** – Combines document retrieval with Gemini
  to generate answers and solutions.
- **LLM** – Connects the application to Google Gemini.
- **Question Bank UI** – Displays extracted questions and
  allows users to generate solutions.
- **Streamlit UI** – Provides the application interface.

## Currently Supported Question Types

The Question Bank currently supports:

- Multiple Choice Questions (MCQ)
- Multiple Select Questions
- Numerical Answer Type Questions

For supported question types, the system can display:

- Question number
- Question text
- Marks
- Options, where applicable
- Question type

The system can also generate solutions for the selected
question.

## Future Enhancements

- Support additional academic question formats
- Improve extraction from complex document layouts
- Improve handling of mathematical notation
- Add more specialized solution-generation strategies
- Improve answer verification and reliability
