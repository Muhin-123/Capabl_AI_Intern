import os
import re


# Subject-level keywords
SUBJECT_KEYWORDS = {
    "DBMS": [
        "database management system",
        "database management",
        "dbms",
        "database system",
        "relational database",
        "sql",
        "database",
    ]
}


# Chapter and topic keywords based on the DBMS study materials
CHAPTER_TOPICS = {
    "Chapter 1: Database System Architecture": {
        "Database System Architecture": [
            "database system architecture",
            "three level architecture",
            "3 level architecture",
            "ansi sparc",
            "ansi-sparc",
        ],
        "Introduction to DBMS": [
            "introduction to dbms",
            "database management system",
            "applications of dbms",
            "advantages of dbms",
        ],
        "Data Abstraction": [
            "data abstraction",
            "physical level",
            "logical level",
            "view level",
        ],
        "Data Independence": [
            "data independence",
            "physical data independence",
            "logical data independence",
        ],
        "Database Users": [
            "database users",
            "end users",
            "application programmers",
        ],
        "Database Administrator": [
            "database administrator",
            "dba",
            "dba role",
            "dba responsibilities",
        ],
    },

    "Chapter 2: Data Models": {
        "ER Model": [
            "er model",
            "entity relationship",
            "entity-relationship",
            "er diagram",
            "erd",
        ],
        "Entities and Attributes": [
            "entity",
            "entities",
            "attribute",
            "attributes",
        ],
        "Relationships": [
            "relationship",
            "relationships",
            "relationship set",
        ],
        "Mapping Cardinality": [
            "mapping cardinality",
            "cardinality",
            "one to one",
            "one-to-one",
            "one to many",
            "one-to-many",
            "many to one",
            "many-to-one",
            "many to many",
            "many-to-many",
        ],
        "Weak Entities": [
            "weak entity",
            "weak entities",
        ],
        "Specialization and Generalization": [
            "specialization",
            "generalization",
        ],
        "Aggregation": [
            "aggregation",
        ],
        "Database Models": [
            "hierarchical model",
            "network model",
            "relational model",
            "object oriented model",
            "object-oriented model",
            "database models",
        ],
    },

    "Chapter 3: Relational Model": {
        "Relational Algebra": [
            "relational algebra",
            "selection",
            "projection",
            "union",
            "intersection",
            "cartesian product",
        ],
        "Keys": [
            "primary key",
            "foreign key",
            "candidate key",
            "super key",
            "composite key",
        ],
        "Integrity Constraints": [
            "integrity constraint",
            "integrity constraints",
            "referential integrity",
            "entity integrity",
        ],
        "Joins": [
            "join",
            "joins",
            "natural join",
            "outer join",
            "inner join",
        ],
    },

    "Chapter 4: Functional Dependencies and Normalization": {
        "Functional Dependency": [
            "functional dependency",
            "functional dependencies",
        ],
        "Armstrong's Axioms": [
            "armstrong",
            "armstrong's axioms",
            "armstrong axioms",
        ],
        "Attribute Closure": [
            "attribute closure",
            "closure of attribute",
        ],
        "Normalization": [
            "normalization",
            "normal forms",
            "1nf",
            "2nf",
            "3nf",
            "bcnf",
            "4nf",
            "5nf",
        ],
        "Decomposition": [
            "decomposition",
            "lossless decomposition",
            "lossless join",
            "dependency preservation",
        ],
    },

    "Chapter 5: SQL": {
        "SQL": [
            "structured query language",
            "sql",
            "sql query",
        ],
        "DDL and DML": [
            "ddl",
            "dml",
            "data definition language",
            "data manipulation language",
        ],
        "SQL Queries": [
            "select statement",
            "select query",
            "insert",
            "update",
            "delete",
            "where clause",
            "group by",
            "order by",
        ],
        "Triggers": [
            "trigger",
            "triggers",
        ],
        "PL/SQL": [
            "pl/sql",
            "plsql",
            "stored procedure",
            "procedure",
            "cursor",
        ],
    },

    "Chapter 6: Transactions": {
        "Transactions": [
            "transaction",
            "transactions",
            "transaction management",
        ],
        "ACID Properties": [
            "acid",
            "atomicity",
            "consistency",
            "isolation",
            "durability",
        ],
        "Serializability": [
            "serializability",
            "serial schedule",
            "conflict serializability",
            "view serializability",
        ],
        "Locks": [
            "lock",
            "locks",
            "shared lock",
            "exclusive lock",
        ],
        "Deadlocks": [
            "deadlock",
            "deadlocks",
        ],
        "Concurrency Control": [
            "concurrency control",
            "concurrent execution",
        ],
    },

    "Chapter 7: Storage, Indexing and Recovery": {
        "Hashing": [
            "hashing",
            "hash function",
            "hash file organization",
        ],
        "B-Trees and B+ Trees": [
            "b-tree",
            "b trees",
            "b+ tree",
            "b+ trees",
        ],
        "Indexing": [
            "indexing",
            "index",
            "primary index",
            "secondary index",
        ],
        "Query Processing": [
            "query processing",
            "query processor",
            "query optimization",
        ],
        "Recovery": [
            "recovery",
            "database recovery",
            "log based recovery",
            "checkpoint",
        ],
    },
}


def normalize_text(text):
    """Normalize text for keyword matching."""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def classify_subject(text, filename=""):
    """
    Identify the subject using document content and filename.
    """

    combined_text = normalize_text(
        f"{filename} {text}"
    )

    scores = {}

    for subject, keywords in SUBJECT_KEYWORDS.items():
        score = 0

        for keyword in keywords:
            if keyword in combined_text:
                score += 1

        scores[subject] = score

    if not scores:
        return "Unknown"

    best_subject = max(scores, key=scores.get)

    if scores[best_subject] == 0:
        return "Unknown"

    return best_subject

def classify_all_topics(text, filename=""):
    """
    Find all chapters and topics that match the document content.
    """

    combined_text = normalize_text(
        f"{filename} {text}"
    )

    results = {}

    for chapter, topics in CHAPTER_TOPICS.items():

        matched_topics = []

        for topic, keywords in topics.items():

            score = sum(
                1 for keyword in keywords
                if keyword in combined_text
            )

            if score > 0:
                matched_topics.append({
                    "topic": topic,
                    "score": score
                })

        if matched_topics:
            matched_topics.sort(
                key=lambda item: item["score"],
                reverse=True
            )

            results[chapter] = matched_topics

    return results


def classify_chapter_and_topic(text, filename=""):
    """
    Find the single strongest chapter and topic.
    """

    all_topics = classify_all_topics(text, filename)

    if not all_topics:
        return "Unknown", "Unknown"

    best_chapter = "Unknown"
    best_topic = "Unknown"
    best_score = 0

    for chapter, topics in all_topics.items():

        for item in topics:

            if item["score"] > best_score:
                best_score = item["score"]
                best_chapter = chapter
                best_topic = item["topic"]

    return best_chapter, best_topic



def classify_document(filename, text):
    """
    Return subject, primary chapter/topic,
    and all detected chapters/topics.
    """

    subject = classify_subject(text, filename)

    primary_chapter, primary_topic = classify_chapter_and_topic(
        text,
        filename
    )

    all_topics = classify_all_topics(text, filename)

    chapters = list(all_topics.keys())

    topics = []

    for chapter_topics in all_topics.values():
        for item in chapter_topics:
            topics.append(item["topic"])

    return {
        "subject": subject,
        "chapter": primary_chapter,
        "topic": primary_topic,
        "chapters": chapters,
        "topics": topics,
    }


if __name__ == "__main__":

    sample_text = """
    Database Management System.
    Three level architecture, data abstraction,
    data independence and database administrator.
    """

    result = classify_document(
        "Unit-1.ppt.pdf",
        sample_text
    )

    print("Subject :", result["subject"])
    print("Chapter :", result["chapter"])
    print("Topic   :", result["topic"])
