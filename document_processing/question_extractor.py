import re


SECTION_PATTERNS = [
    (
        "mcq_1_mark",
        "Multiple Choice Questions (1 Mark)",
        1,
        "mcq",
    ),
    (
        "mcq_2_mark",
        "Multiple Choice Questions (2 Marks)",
        2,
        "mcq",
    ),
    (
        "multiple_select_2_mark",
        "Multiple Select Questions (2 Marks)",
        2,
        "multiple_select",
    ),
    (
        "numerical_2_mark",
        "Numerical Answer Type Questions (2 Marks)",
        2,
        "numerical",
    ),
]


def normalize_text(text):
    """Normalize whitespace while preserving enough structure for parsing."""

    text = text.replace("\r", "\n")

    # Normalize common OCR/extraction artifacts.
    text = text.replace("￾", "")
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    # Collapse repeated whitespace.
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines.
    text = re.sub(r"\n\s*\n+", "\n", text)

    return text.strip()


def detect_sections(text):
    """
    Detect question-paper sections.

    Returns:
        List of tuples:
        (section_start, section_end, section_id, section_name, marks, type)
    """

    sections = []

    patterns = [
        (
            r"Multiple Choice Questions\s*\(1\s*Marks?\)",
            "mcq_1_mark",
            "Multiple Choice Questions (1 Mark)",
            1,
            "mcq",
        ),
        (
            r"Multiple Choice Questions\s*\(2\s*Marks?\)",
            "mcq_2_mark",
            "Multiple Choice Questions (2 Marks)",
            2,
            "mcq",
        ),
        (
            r"Multiple Select Questions\s*\(2\s*Marks?\)",
            "multiple_select_2_mark",
            "Multiple Select Questions (2 Marks)",
            2,
            "multiple_select",
        ),
        (
            r"Numerical Answer Type Questions\s*\(2\s*Marks?\)",
            "numerical_2_mark",
            "Numerical Answer Type Questions (2 Marks)",
            2,
            "numerical",
        ),
    ]

    for pattern, section_id, section_name, marks, question_type in patterns:

        for match in re.finditer(pattern, text, re.IGNORECASE):

            sections.append(
                (
                    match.start(),
                    match.end(),
                    section_id,
                    section_name,
                    marks,
                    question_type,
                )
            )

    sections.sort(key=lambda item: item[0])

    return sections


def extract_options(question_text):
    """
    Extract A/B/C/D options from an MCQ.
    """

    options = {}

    option_pattern = re.compile(
        r"(?:^|\s)([A-D])\.\s*(.*?)(?=\s+[A-D]\.\s|$)",
        re.IGNORECASE,
    )

    matches = option_pattern.findall(question_text)

    for letter, value in matches:
        options[letter.upper()] = value.strip()

    return options


def clean_question_text(question_text):
    """Clean extracted question text."""

    question_text = question_text.strip()

    # Remove accidental whitespace.
    question_text = re.sub(r"\s+", " ", question_text)

    # Remove obvious trailing artifacts.
    question_text = question_text.strip(" -:")

    return question_text


def parse_numbered_questions(
    section_text,
    section_id,
    section_name,
    marks,
    question_type,
):
    """
    Extract numbered questions from a section.

    Example:
        1. Question...
        2. Question...
        3. Question...
    """

    questions = []

    pattern = re.compile(
        r"(?:^|\s)(\d+)\.\s+(.*?)(?=\s+\d+\.\s+|$)",
        re.DOTALL,
    )

    matches = list(pattern.finditer(section_text))

    for match in matches:

        question_number = int(match.group(1))
        raw_content = match.group(2).strip()

        if not raw_content:
            continue

        options = {}

        if question_type in {"mcq", "multiple_select"}:

            options = extract_options(raw_content)

            # Remove options from the question text.
            question_text = re.split(
                r"\s+[A-D]\.\s+",
                raw_content,
                maxsplit=1,
                flags=re.IGNORECASE,
            )[0]

        else:
            question_text = raw_content

        question_text = clean_question_text(question_text)

        # Ignore malformed entries.
        if len(question_text) < 5:
            continue

        question = {
            "id": f"{section_id}_{question_number}",
            "section": section_name,
            "question_number": question_number,
            "question": question_text,
            "options": options,
            "marks": marks,
            "type": question_type,
        }

        questions.append(question)

    return questions


def extract_questions(text):
    """
    Extract structured questions from an academic question paper.

    Returns a list of dictionaries suitable for the Question Bank UI.
    """

    if not text or not text.strip():
        return []

    text = normalize_text(text)

    sections = detect_sections(text)

    if not sections:
        return []

    all_questions = []

    for index, section in enumerate(sections):

        start = section[1]

        if index + 1 < len(sections):
            end = sections[index + 1][0]
        else:
            end = len(text)

        section_text = text[start:end]

        (
            _,
            _,
            section_id,
            section_name,
            marks,
            question_type,
        ) = section

        questions = parse_numbered_questions(
            section_text=section_text,
            section_id=section_id,
            section_name=section_name,
            marks=marks,
            question_type=question_type,
        )

        all_questions.extend(questions)

    return all_questions