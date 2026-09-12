import re


# ============================================================
# SECTION DEFINITIONS
# ============================================================

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


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    """
    Normalize extracted document text while preserving
    enough structure for question parsing.
    """

    text = text.replace("\r", "\n")

    # Remove common extraction artifacts.
    text = text.replace("￾", "")

    # Normalize dash characters.
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    # Collapse repeated spaces/tabs.
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines.
    text = re.sub(r"\n\s*\n+", "\n", text)

    return text.strip()


# ============================================================
# SECTION DETECTION
# ============================================================

def detect_sections(text):
    """
    Detect question-paper sections.

    Returns:
        List of tuples:

        (
            section_start,
            section_end,
            section_id,
            section_name,
            marks,
            question_type
        )
    """

    sections = []

    patterns = [
        (
            r"Multiple Choice Questions\s*\(?1\s*Marks?\)?",
            "mcq_1_mark",
            "Multiple Choice Questions (1 Mark)",
            1,
            "mcq",
        ),
        (
            r"Multiple Choice Questions\s*\(?2\s*Marks?\)?",
            "mcq_2_mark",
            "Multiple Choice Questions (2 Marks)",
            2,
            "mcq",
        ),
        (
            r"Multiple Select Questions\s*\(?2\s*Marks?\)?",
            "multiple_select_2_mark",
            "Multiple Select Questions (2 Marks)",
            2,
            "multiple_select",
        ),
        (
            r"Numerical Answer Type Questions\s*\(?2\s*Marks?\)?",
            "numerical_2_mark",
            "Numerical Answer Type Questions (2 Marks)",
            2,
            "numerical",
        ),
    ]

    for (
        pattern,
        section_id,
        section_name,
        marks,
        question_type,
    ) in patterns:

        for match in re.finditer(
            pattern,
            text,
            re.IGNORECASE,
        ):

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

    sections.sort(
        key=lambda item: item[0]
    )

    return sections


# ============================================================
# OPTION EXTRACTION
# ============================================================

def extract_options(question_text):
    """
    Extract A/B/C/D options from an MCQ.

    Supports extracted PDF text where there may be
    inconsistent spacing after the option letter.
    """

    options = {}

    option_pattern = re.compile(
        r"(?:^|\s)([A-D])\.\s*(.*?)(?=\s+[A-D]\.\s|$)",
        re.IGNORECASE | re.DOTALL,
    )

    matches = option_pattern.findall(
        question_text
    )

    for letter, value in matches:

        value = clean_question_text(
            value
        )

        if value:
            options[letter.upper()] = value

    return options


# ============================================================
# QUESTION TEXT CLEANING
# ============================================================

def clean_question_text(question_text):
    """
    Clean extracted question text.
    """

    question_text = question_text.strip()

    # Normalize repeated whitespace.
    question_text = re.sub(
        r"\s+",
        " ",
        question_text,
    )

    # Remove obvious trailing punctuation/artifacts.
    question_text = question_text.strip(
        " -:"
    )

    return question_text


# ============================================================
# NUMBERED QUESTION PARSING
# ============================================================

def parse_numbered_questions(
    section_text,
    section_id,
    section_name,
    marks,
    question_type,
):
    """
    Extract numbered questions from a section.

    Supports both:

        1. Question text
        2. Question text

    and PDF-extracted variants such as:

        1.Question text
        2.Question text
    """

    questions = []

    # --------------------------------------------------------
    # IMPORTANT:
    #
    # Use \s* after the period instead of \s+.
    #
    # PDF extraction may produce:
    #
    #   10.Consider...
    #
    # instead of:
    #
    #   10. Consider...
    #
    # Using \s* allows both formats.
    # --------------------------------------------------------

    pattern = re.compile(
        r"(?:^|\s)(\d+)\.\s*(.*?)(?=\s+\d+\.\s*|$)",
        re.DOTALL,
    )

    matches = list(
        pattern.finditer(section_text)
    )

    for match in matches:

        question_number = int(
            match.group(1)
        )

        raw_content = match.group(2).strip()

        if not raw_content:
            continue

        options = {}

        # ----------------------------------------------------
        # MCQ / MULTIPLE SELECT
        # ----------------------------------------------------

        if question_type in {
            "mcq",
            "multiple_select",
        }:

            options = extract_options(
                raw_content
            )

            # Remove options from the question text.
            question_text = re.split(
                r"\s+[A-D]\.\s*",
                raw_content,
                maxsplit=1,
                flags=re.IGNORECASE,
            )[0]

        # ----------------------------------------------------
        # NUMERICAL / OTHER
        # ----------------------------------------------------

        else:

            question_text = raw_content

        question_text = clean_question_text(
            question_text
        )

        # ----------------------------------------------------
        # IGNORE MALFORMED ENTRIES
        # ----------------------------------------------------

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

        questions.append(
            question
        )

    return questions


# ============================================================
# MAIN QUESTION EXTRACTION
# ============================================================

def extract_questions(text):
    """
    Extract structured questions from an academic
    question paper.

    Returns:
        List of dictionaries suitable for the
        Question Bank UI.
    """

    if not text or not text.strip():
        return []

    # --------------------------------------------------------
    # STEP 1 — NORMALIZE TEXT
    # --------------------------------------------------------

    text = normalize_text(text)

    # --------------------------------------------------------
    # STEP 2 — DETECT SECTIONS
    # --------------------------------------------------------

    sections = detect_sections(text)

    if not sections:
        return []

    all_questions = []

    # --------------------------------------------------------
    # STEP 3 — PARSE EACH SECTION
    # --------------------------------------------------------

    for index, section in enumerate(
        sections
    ):

        start = section[1]

        if index + 1 < len(sections):

            end = sections[index + 1][0]

        else:

            end = len(text)

        section_text = text[
            start:end
        ]

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

        all_questions.extend(
            questions
        )

    return all_questions