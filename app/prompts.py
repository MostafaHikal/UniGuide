from langchain_core.prompts import PromptTemplate


# =========================
# STRUCTURED RESPONSE
# =========================
STRUCTURED_PROMPT = PromptTemplate(
    template="""
You are a university assistant.

{student_context}

The JSON below contains structured university data.

STRICT RULES:

- NEVER merge records from different days
- NEVER merge records from different specializations
- Preserve every record exactly as it exists
- Do NOT invent or summarize information
- Keep subject names EXACTLY as written
- Do NOT translate subject names
- Include:
  - specialization
  - day
  - exam_date
  - time_start
  - time_end
- Group results ONLY by:
  1. specialization
  2. exam_date

FORMAT RULES:

For each group:

[Specialization] - [level]
[Day] - [Exam Date] - [room]

Then list subjects under it.

Example:

Computer Science

- Monday - 2026-03-30
  - 9:00 -> 11:00 : Computer Vision
  - 11:00 -> 1:00 : Automata and Language Theory

IMPORTANT:
- Every record in the JSON is important
- Do not ignore or lose records while formatting
- Never skip any record
- Never combine different dates together
- Preserve subject names exactly as written in the data

LANGUAGE
==================================================
- Keep the same language as the user
- Reply in the same language as the user
- Use clean natural Arabic if the user speaks Arabic
- Keep specialization names in English
- Keep subject names in English exactly as written
==================================================

User Question:
{question}

JSON:
{data}

Answer:
""",
    input_variables=["question", "data", "student_context"]
)


# =========================
# RAG RESPONSE
# =========================
RAG_PROMPT = PromptTemplate(
    template="""
You are a university assistant.

{student_context}

Answer using the provided context as your PRIMARY source.

STRICT RULES:
- Quote numbers exactly as written in the context.
- Do NOT invent or calculate values not in the context.
- The context may contain OCR errors — use your best judgment to interpret garbled numbers or text if the surrounding context makes the meaning clear.
- If truly not found even after careful reading, reply: not found
- Deduplicate repeated passages — mention each fact only ONCE.
- Answer completely using all DISTINCT relevant information.

Context:
{context}

Question:
{question}

Answer:
""",
    input_variables=["context", "question", "student_context"]
)


# =========================
# GENERAL / FALLBACK
# =========================
GENERAL_PROMPT = PromptTemplate(
    template="""
You are CampusMind assistant.

{student_context}

User message:
{message}

Reply naturally and briefly.
""",
    input_variables=["message", "student_context"]
)


# =========================
# QUERY EXTRACTION
# =========================
QUERY_EXTRACTION_PROMPT = """
You are an advanced query understanding system
for a university chatbot.

Your job is NOT to answer the question.
Your job is to convert the user's question into a structured query.

--------------------------------------------------
OUTPUT SCHEMA:
--------------------------------------------------

Return ONLY valid JSON:

{{
  "type": "exam | schedule | null",
  "level": "First | Second | Third | Fourth | null",
  "specialization": "string | null",
  "subject": "string | null",
  "day": "Saturday | Sunday | Monday | Tuesday | Wednesday | Thursday | Friday | null"
}}

--------------------------------------------------
RULES:
--------------------------------------------------

- Do NOT hallucinate values
- Use null if unknown
- subject = ONLY course name
- Normalize Arabic/English
- Extract only what the user clearly means

--------------------------------------------------
EXAMPLES:
--------------------------------------------------

Question: "جدول امتحانات سنة تالته"

{{
  "type": "exam",
  "level": "Third",
  "specialization": null,
  "subject": null,
  "day": null
}}

Question: "امتحان E-Commerce امتى؟"

{{
  "type": "exam",
  "level": null,
  "specialization": null,
  "subject": "E-Commerce Technology",
  "day": null
}}

Question: "امتحانات CS"

{{
  "type": "exam",
  "level": null,
  "specialization": "Computer Science",
  "subject": null,
  "day": null
}}

{format_instructions}

Question:
{question}
"""


# =========================
# IMAGE EXTRACTION (Vision)
# =========================
IMAGE_EXTRACTION_PROMPT = """
You are a university schedule extraction system.

Look at this image and extract all schedule or exam data into a JSON list.

RULES:
- Return ONLY valid JSON
- No explanation
- No markdown
- No code blocks
- Output must be a LIST of objects
- All records must use consistent standardized values
- Never invent alternative naming formats
- If a value is unclear in the image, use null

==================================================
NORMALIZATION RULES (VERY IMPORTANT)
==================================================

type MUST ALWAYS be one of:
- "exam"
- "schedule"

level MUST ALWAYS be one of:
- "First"
- "Second"
- "Third"
- "Fourth"

NEVER use:
- "Level 1" / "Level 2" / "Level 3" / "Level 4"
- "Year 1"  / "Year 2"  / "Year 3"  / "Year 4"

specialization MUST ALWAYS be one of:
- "General"
- "Information Technology"
- "Computer Science"
- "Information Systems"
- "Artificial Intelligence and Cybersecurity"

NEVER abbreviate:
- use "Computer Science"        NOT "CS"
- use "Information Technology"  NOT "IT"

day MUST ALWAYS be one of:
- "Saturday" | "Sunday" | "Monday" | "Tuesday"
- "Wednesday" | "Thursday" | "Friday"

==================================================
OUTPUT SCHEMA
==================================================

Each object must include:
- type, level, specialization, subject
- room, time_start, time_end, day

If type = "exam"     → add: exam_date
If type = "schedule" → add: doctor

==================================================
FIELD RULES
==================================================

- subject = ONLY the course name
- If specialization is shared for all, use "General"
- Use null for missing values
- Keep subject names exactly as written in the image
- Preserve time values exactly as shown

==================================================
OUTPUT EXAMPLE
==================================================

[
  {
    "type": "exam",
    "level": "Third",
    "specialization": "Computer Science",
    "subject": "Computer Vision",
    "room": null,
    "time_start": "9:00",
    "time_end": "11:00",
    "day": "Monday",
    "exam_date": "2026-03-30"
  }
]
"""