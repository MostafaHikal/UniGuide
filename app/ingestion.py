import os
import json
import base64
import uuid

from pdf2image import convert_from_path
import pytesseract

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from groq import Groq

from app.normalizer import normalize_record
from app.prompts import IMAGE_EXTRACTION_PROMPT
from app.config import (
    MODEL_NAME, GROQ_API_KEY, VISION_MODEL, EMBEDDING_MODEL,
    VECTOR_STORE_PATH, TABLES_JSON_PATH,
    POPPLER_PATH, OCR_DPI, OCR_LANG,
    CHUNK_SIZE, CHUNK_OVERLAP
)


# =========================
# LLM
# =========================
llm = ChatGroq(
    temperature=0,
    model_name=MODEL_NAME,
    groq_api_key=GROQ_API_KEY,
)

vision_client = Groq(api_key=GROQ_API_KEY)


# =========================
# 1. IMAGE → base64
# =========================
def image_to_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


# =========================
# 2. IMAGE → JSON (Vision)
# =========================
def extract_table_json_from_image(file_path):

    image_data = image_to_base64(file_path)
    ext        = file_path.lower().split(".")[-1]
    media_type = "image/jpeg" if ext in ("jpg", "jpeg") else "image/png"

    response = vision_client.chat.completions.create(
        model=VISION_MODEL,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{media_type};base64,{image_data}"}
                },
                {
                    "type": "text",
                    "text": IMAGE_EXTRACTION_PROMPT
                }
            ]
        }],
        temperature=0,
    )

    raw = response.choices[0].message.content.strip()

    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    try:
        return json.loads(raw)
    except Exception as e:
        print(f"Error parsing JSON from image: {e}")
        return []


# =========================
# 3. SAVE JSON
# =========================
def save_json(data):

    os.makedirs("data", exist_ok=True)

    if not isinstance(data, list):
        return "invalid data"

    old_data = []
    if os.path.exists(TABLES_JSON_PATH):
        with open(TABLES_JSON_PATH, "r", encoding="utf-8") as f:
            old_data = json.load(f)

    def is_duplicate(record, existing_records):
        for existing in existing_records:
            if (
                record.get("subject") == existing.get("subject")
                and record.get("day") == existing.get("day")
                and record.get("level") == existing.get("level")
                and record.get("specialization") == existing.get("specialization")
            ):
                return True
        return False

    new_records = [r for r in data if not is_duplicate(r, old_data)]
    old_data.extend(new_records)

    with open(TABLES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(old_data, f, ensure_ascii=False, indent=2)

    return f"saved {len(new_records)} new records, skipped {len(data) - len(new_records)} duplicates"


# =========================
# 4. SAVE VECTOR DB
# =========================
def save_to_vector_db(chunks):

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    os.makedirs("vector_store", exist_ok=True)

    if os.path.exists(VECTOR_STORE_PATH):
        vector_db = FAISS.load_local(
            VECTOR_STORE_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )
        vector_db.add_documents(chunks)
    else:
        vector_db = FAISS.from_documents(chunks, embeddings)

    vector_db.save_local(VECTOR_STORE_PATH)
    return "saved vector db"


# =========================
# 5. INGEST IMAGE
# =========================
def ingest_image(file_path):

    data = extract_table_json_from_image(file_path)

    if not data:
        return "skipped - no data extracted"

    normalized_data = [normalize_record(record) for record in data]

    return save_json(normalized_data)


def fix_arabic_numerals(text: str) -> str:
    arabic_indic = '٠١٢٣٤٥٦٧٨٩'
    western      = '0123456789'
    table = str.maketrans(arabic_indic, western)
    return text.translate(table)


# =========================
# 6. INGEST PDF
# =========================
def ingest_pdf(file_path):

    pages = convert_from_path(
        file_path,
        dpi=OCR_DPI,
        poppler_path=POPPLER_PATH
    )

    docs = []

    for page_number, page in enumerate(pages):

        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(page, lang=OCR_LANG)

        text = fix_arabic_numerals(text)

        if not text.strip():
            continue

        docs.append(Document(
            page_content=text,
            metadata={
                "page":   page_number + 1,
                "source": os.path.basename(file_path)
            }
        ))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " "]
    )

    chunks = splitter.split_documents(docs)

    for i, chunk in enumerate(chunks):
        chunk.metadata.update({
            "source":   os.path.basename(file_path),
            "chunk_id": i,
            "id":       str(uuid.uuid4())
        })

    return save_to_vector_db(chunks)


# =========================
# 7. INGEST (single file)
# =========================
def ingest(file_path):

    file_path_lower = file_path.lower()

    if file_path_lower.endswith((".png", ".jpg", ".jpeg")):
        return ingest_image(file_path)

    elif file_path_lower.endswith(".pdf"):
        return ingest_pdf(file_path)

    else:
        raise ValueError(f"Unsupported file type: {file_path}")


# =========================
# 8. INGEST FOLDER
# =========================
def ingest_folder(folder_path):

    results = []

    for root, dirs, files in os.walk(folder_path):
        for file_name in files:

            file_path = os.path.join(root, file_name)

            if not file_name.lower().endswith((".png", ".jpg", ".jpeg", ".pdf")):
                continue

            try:
                result = ingest(file_path)
                results.append({"file": file_path, "status": result})

            except Exception as e:
                results.append({"file": file_path, "status": f"error: {e}"})

    return results


# =========================
# TEST
# =========================
if __name__ == "__main__":

    results_college = ingest_folder("data/College")
    results_tables  = ingest_folder("data/Tables")

    all_results = results_college + results_tables
    passed = [r for r in all_results if "error" not in r["status"]]
    failed = [r for r in all_results if "error" in r["status"]]

    print(f"Done: {len(passed)} succeeded, {len(failed)} failed")

    if failed:
        for r in failed:
            print(f"  {r['file']}: {r['status']}")