from datetime import datetime

# =========================
# LEVEL NORMALIZATION
# =========================
LEVEL_MAP = {
    "first": "First",
    "1st": "First",
    "first year": "First",
    "year 1": "First",
    "سنة اولى": "First",
    "اولى": "First",

    "second": "Second",
    "2nd": "Second",
    "second year": "Second",
    "year 2": "Second",
    "تانية": "Second",
    "سنة تانية": "Second",

    "third": "Third",
    "3rd": "Third",
    "third year": "Third",
    "year 3": "Third",
    "تالتة": "Third",
    "سنة تالته": "Third",

    "fourth": "Fourth",
    "4th": "Fourth",
    "fourth year": "Fourth",
    "year 4": "Fourth",
    "رابعة": "Fourth",
    "سنة رابعة": "Fourth",
}


# =========================
# TYPE NORMALIZATION
# =========================
TYPE_MAP = {
    "exam": "exam",
    "exams": "exam",
    "test": "exam",
    "امتحان": "exam",
    "امتحانات": "exam",

    "schedule": "schedule",
    "timetable": "schedule",
    "lecture": "schedule",
    "lectures": "schedule",
    "محاضرة": "schedule",
    "جدول": "schedule",
}


# =========================
# DAY NORMALIZATION
# =========================
DAY_MAP = {
    "saturday": "Saturday",
    "sat": "Saturday",
    "السبت": "Saturday",

    "sunday": "Sunday",
    "sun": "Sunday",
    "الاحد": "Sunday",
    "الأحد": "Sunday",

    "monday": "Monday",
    "mon": "Monday",
    "الاتنين": "Monday",
    "الاثنين": "Monday",

    "tuesday": "Tuesday",
    "tue": "Tuesday",
    "tues": "Tuesday",
    "الترتي": "Tuesday",
    "الثلاثاء": "Tuesday",

    "wednesday": "Wednesday",
    "wed": "Wednesday",
    "الاربعاء": "Wednesday",
    "الأربعاء": "Wednesday",

    "thursday": "Thursday",
    "thu": "Thursday",
    "thurs": "Thursday",
    "الخميس": "Thursday",

    "friday": "Friday",
    "fri": "Friday",
    "الجمعة": "Friday",
}


# =========================
# SPECIALIZATION NORMALIZATION
# =========================
SPECIALIZATION_MAP = {
    "it": "Information Technology",
    "i.t": "Information Technology",
    "information technology": "Information Technology",
    "information tech": "Information Technology",
    "تكنولوجيا المعلومات": "Information Technology",

    "cs": "Computer Science",
    "c.s": "Computer Science",
    "computer science": "Computer Science",

    "ai": "Artificial Intelligence and Cybersecurity",
    "a.i": "Artificial Intelligence and Cybersecurity",
    "artificial intelligence": "Artificial Intelligence and Cybersecurity",

    "cyber": "Artificial Intelligence and Cybersecurity",
    "cybersecurity": "Artificial Intelligence and Cybersecurity",
    "cyber security": "Artificial Intelligence and Cybersecurity",

    "ai and cyber": "Artificial Intelligence and Cybersecurity",
    "ai & cyber": "Artificial Intelligence and Cybersecurity",
}


# =========================
# CORE NORMALIZER FUNCTION
# =========================
def normalize_value(value, mapping):
    if value is None:
        return None

    if isinstance(value, str):
        value = value.lower().strip()
    else:
        return None

    return mapping.get(value, value)


# =========================
# MAIN NORMALIZATION PIPELINE
# =========================
def normalize_query(query: dict) -> dict:

    if not query:
        return query

    return {
        "type": normalize_value(query.get("type"), TYPE_MAP),
        "level": normalize_value(query.get("level"), LEVEL_MAP),
        "specialization": normalize_value(query.get("specialization"), SPECIALIZATION_MAP),
        "subject": query.get("subject"),
        "day": normalize_value(query.get("day"), DAY_MAP),
    }

# =========================
# DATE NORMALIZATION
# =========================
def normalize_date(date_value):

    if not date_value:
        return None

    if not isinstance(date_value, str):
        return None

    date_value = date_value.strip()

    formats = [
        "%Y-%m-%d",
        "%Y-%m-%d",
        "%Y-%#m-%#d",   # windows
    ]

    for fmt in formats:
        try:
            parsed = datetime.strptime(date_value, fmt)

            # ALWAYS RETURN:
            # 2026-03-31
            return parsed.strftime("%Y-%m-%d")

        except:
            continue

    return date_value

# =========================
# RECORD NORMALIZATION
# =========================
def normalize_record(record: dict):

    if not record:
        return record

    return {
        "type": normalize_value(record.get("type"), TYPE_MAP),

        "level": normalize_value(
            record.get("level"),
            LEVEL_MAP
        ),

        "specialization": normalize_value(
            record.get("specialization"),
            SPECIALIZATION_MAP
        ),

        # IMPORTANT:
        # keep subject as-is
        "subject": (
            record.get("subject").strip()
            if record.get("subject")
            else None
        ),

        "room": record.get("room"),

        "time_start": record.get("time_start"),

        "time_end": record.get("time_end"),

        "day": normalize_value(
            record.get("day"),
            DAY_MAP
        ),

        # 🔥 IMPORTANT FIX
        "exam_date": normalize_date(
            record.get("exam_date")
        ),

        "doctor": record.get("doctor")
    }