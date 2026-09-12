import re


SUBJECT_KEYWORDS = {
    "DBMS": [
        "database management system",
        "database management",
        "dbms",
        "database system",
        "relational database",
        "sql",
        "database",
        "mysql",
        "postgresql",
        "oracle",
        "normalization",
        "primary key",
        "foreign key",
        "er diagram",
        "transaction",
    ],

    "Data Structures and Algorithms": [
        "data structure",
        "algorithm",
        "array",
        "linked list",
        "stack",
        "queue",
        "tree",
        "binary tree",
        "graph",
        "sorting",
        "searching",
        "recursion",
    ],

    "Operating Systems": [
        "operating system",
        "process",
        "thread",
        "deadlock",
        "cpu scheduling",
        "process scheduling",
        "memory management",
        "paging",
        "segmentation",
        "virtual memory",
        "file system",
    ],

    "Computer Networks": [
        "computer network",
        "networking",
        "tcp",
        "udp",
        "ip address",
        "routing",
        "osi model",
        "tcp/ip",
        "subnetting",
        "network protocol",
        "ethernet",
    ],

    "Aptitude": [
        "aptitude",
        "quantitative aptitude",
        "logical reasoning",
        "verbal ability",
        "engineering aptitude",
        "comprehensive engineering aptitude",
        "percentage",
        "profit and loss",
        "ratio",
        "proportion",
        "time and work",
        "probability",
        "permutation",
        "combination",
        "number system",
    ],

    "Artificial Intelligence and Machine Learning": [
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "neural network",
        "cnn",
        "rnn",
        "classification",
        "regression",
        "supervised learning",
        "unsupervised learning",
        "computer vision",
    ],
}


CHAPTER_TOPICS = {
    "Chapter 1: Database System Architecture": {
        "Introduction to DBMS": [
            "introduction of dbms",
            "introduction to dbms",
            "database management system",
            "applications of dbms",
            "advantages of dbms",
        ],

        "Database System Architecture": [
            "database system architecture",
            "three level architecture",
            "3 level architecture",
            "ansi sparc",
            "ansi-sparc",
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
            "types of database users",
            "naive users",
            "end users",
            "application programmers",
            "sophisticated users",
            "specialized users",
        ],

        "Database Administrator": [
            "database administrator",
            "dba",
            "role of dba",
            "roles of dba",
            "dba responsibilities",
            "tasks of dba",
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
            "selection operation",
            "projection operation",
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

        "Join Operation": [
            "join operation",
            "natural join",
            "outer join",
            "inner join",
            "left outer join",
            "right outer join",
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
            "sql query",
            "sql statement",
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
            "insert into",
            "update statement",
            "delete statement",
            "where clause",
            "group by",
            "order by",
        ],

        "Triggers": [
            "trigger",
            "triggers",
            "database trigger",
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
            "transaction management",
            "transaction processing",
            "transaction schedule",
        ],

        "ACID Properties": [
            "acid properties",
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
            "shared lock",
            "exclusive lock",
            "lock based protocol",
            "two phase locking",
        ],

        "Deadlocks": [
            "deadlock",
            "deadlocks",
            "deadlock detection",
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
            "primary index",
            "secondary index",
            "dense index",
            "sparse index",
        ],

        "Query Processing": [
            "query processing",
            "query processor",
            "query optimization",
        ],

        "Recovery": [
            "database recovery",
            "log based recovery",
            "checkpoint",
            "recovery techniques",
        ],
    },
}


def normalize_text(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def classify_subject(text, filename=""):
    combined_text = normalize_text(
        f"{filename} {text}"
    )

    # Give clear Aptitude documents priority.
    if (
        "aptitude" in combined_text
        or "comprehensive engineering aptitude test" in combined_text
        or "quantitative aptitude" in combined_text
        or "logical reasoning" in combined_text
        or "verbal aptitude" in combined_text
    ):
        return "Aptitude"

    scores = {}

    for subject, keywords in SUBJECT_KEYWORDS.items():
        score = 0

        for keyword in keywords:
            if keyword.lower() in combined_text:
                score += 1

        scores[subject] = score

    if not scores:
        return "Unknown"

    best_subject = max(scores, key=scores.get)

    if scores[best_subject] == 0:
        return "Unknown"

    return best_subject


def classify_all_topics(text, filename=""):
    combined_text = normalize_text(
        f"{filename} {text}"
    )

    results = {}

    for chapter, topics in CHAPTER_TOPICS.items():

        matched_topics = []

        for topic, keywords in topics.items():

            score = 0

            for keyword in keywords:
                if keyword.lower() in combined_text:
                    score += 1

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


def detect_unit_number(text, filename=""):
    combined_text = normalize_text(
        f"{filename} {text}"
    )

    match = re.search(
        r"\bunit\s*[-:]?\s*(\d+)\b",
        combined_text
    )

    if match:
        return int(match.group(1))

    return None


def classify_chapter_and_topic(text, filename=""):
    all_topics = classify_all_topics(
        text,
        filename
    )

    if not all_topics:
        return "Unknown", "Unknown"

    unit_number = detect_unit_number(
        text,
        filename
    )

    if unit_number is not None:

        chapter_prefix = f"Chapter {unit_number}:"

        for chapter, topics in all_topics.items():

            if chapter.startswith(chapter_prefix):

                if not topics:
                    return chapter, "Unknown"

                combined_text = normalize_text(text)

                topic_positions = []

                for item in topics:

                    topic = item["topic"]
                    keywords = CHAPTER_TOPICS[chapter][topic]

                    positions = []

                    for keyword in keywords:

                        position = combined_text.find(
                            keyword.lower()
                        )

                        if position != -1:
                            positions.append(position)

                    if positions:
                        topic_positions.append(
                            (
                                min(positions),
                                item["topic"]
                            )
                        )

                if topic_positions:

                    topic_positions.sort(
                        key=lambda item: item[0]
                    )

                    return (
                        chapter,
                        topic_positions[0][1]
                    )

                return chapter, topics[0]["topic"]

    # Fallback when there is no clear Unit number.
    best_chapter = "Unknown"
    best_topic = "Unknown"
    best_score = 0

    for chapter, topics in all_topics.items():

        chapter_score = sum(
            item["score"]
            for item in topics
        )

        if chapter_score > best_score:

            best_score = chapter_score
            best_chapter = chapter
            best_topic = topics[0]["topic"]

    return best_chapter, best_topic


def classify_document(filename, text):
    subject = classify_subject(
        text,
        filename
    )

    primary_chapter, primary_topic = (
        classify_chapter_and_topic(
            text,
            filename
        )
    )

    all_topics = classify_all_topics(
        text,
        filename
    )

    unit_number = detect_unit_number(
        text,
        filename
    )

    # If a clear Unit number exists,
    # keep only that chapter.
    if unit_number is not None:

        chapter_prefix = f"Chapter {unit_number}:"

        filtered_topics = {}

        for chapter, chapter_topics in all_topics.items():

            if chapter.startswith(chapter_prefix):
                filtered_topics[chapter] = chapter_topics

        if filtered_topics:
            all_topics = filtered_topics

    chapters = list(
        all_topics.keys()
    )

    topics = []

    for chapter_topics in all_topics.values():

        for item in chapter_topics:
            topics.append(
                item["topic"]
            )

    return {
        "subject": subject,
        "chapter": primary_chapter,
        "topic": primary_topic,
        "chapters": chapters,
        "topics": topics
    }


if __name__ == "__main__":

    sample_text = """
    Database Management System.
    Unit - 1 Database System Architecture.
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
    print("Chapters:", result["chapters"])
    print("Topics  :", result["topics"])