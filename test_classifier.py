from document_processing.processor import process_document
from document_processing.classifier import classify_document
import glob
import os


files = glob.glob("samples/**/*", recursive=True)

for file_path in files:

    if not file_path.lower().endswith((".pdf", ".docx", ".pptx")):
        continue

    result = process_document(file_path)

    if result.get("error"):
        print(f"\n{os.path.basename(file_path)}")
        print("Error:", result["error"])
        continue

    classification = classify_document(
        file_path,
        result.get("text", "")
    )

    print("\n" + "=" * 60)
    print("File    :", os.path.basename(file_path))
    print("Subject :", classification["subject"])
    print("Chapter :", classification["chapter"])
    print("Topic   :", classification["topic"])

    print("\nAll Chapters:")
    for chapter in classification["chapters"]:
        print("-", chapter)

    print("\nAll Topics:")
    for topic in classification["topics"]:
        print("-", topic)