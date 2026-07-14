import os
import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from rapidfuzz import fuzz

from app.normalizer import normalize_query
from app.prompts import QUERY_EXTRACTION_PROMPT
from app.config import (
    MODEL_NAME, GROQ_API_KEY, EMBEDDING_MODEL,
    VECTOR_STORE_PATH, TABLES_JSON_PATH,
    RAG_TOP_K, RAG_FETCH_K, FUZZY_THRESHOLD
)


# =========================
# GLOBALS
# =========================
_embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

_vector_db = None

if os.path.exists(VECTOR_STORE_PATH):
    _vector_db = FAISS.load_local(
        VECTOR_STORE_PATH,
        _embeddings,
        allow_dangerous_deserialization=True
    )
else:
    print("⚠️ Vector DB not found. Please run ingestion first.")


llm = ChatGroq(
    temperature=0,
    model_name=MODEL_NAME,
    groq_api_key=GROQ_API_KEY,
)


# =========================
# 1. STRUCTURED RETRIEVAL
# =========================
def filter_json_data(query):

    if not os.path.exists(TABLES_JSON_PATH):
        return {"status": "not_found", "results": []}

    with open(TABLES_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    query_type           = (query.get("type")           or "").lower().strip()
    query_subject        = (query.get("subject")        or "").lower().strip()
    query_level          = (query.get("level")          or "").lower().strip()
    query_specialization = (query.get("specialization") or "").lower().strip()
    query_day            = (query.get("day")            or "").lower().strip()

    matches = []

    for record in data:

        record_type           = (record.get("type")           or "").lower().strip()
        record_subject        = (record.get("subject")        or "").lower().strip()
        record_level          = (record.get("level")          or "").lower().strip()
        record_specialization = (record.get("specialization") or "").lower().strip()
        record_day            = (record.get("day")            or "").lower().strip()

        type_match = (record_type == query_type) if query_type else True

        subject_match = (
            fuzz.token_set_ratio(query_subject, record_subject) >= FUZZY_THRESHOLD
        ) if query_subject else True

        level_match          = (record_level          == query_level)          if query_level          else True
        specialization_match = (record_specialization == query_specialization) if query_specialization else True
        day_match            = (record_day            == query_day)            if query_day            else True

        if type_match and subject_match and level_match and specialization_match and day_match:
            matches.append(record)

    if not matches:
        return {"status": "not_found", "results": []}

    return {"status": "found", "results": matches, "count": len(matches)}


# =========================
# 2. QUERY EXTRACTION
# =========================
def extract_query_from_question(question):

    parser = JsonOutputParser()

    prompt = PromptTemplate(
        template=QUERY_EXTRACTION_PROMPT,
        input_variables=["question"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        }
    )

    chain = prompt | llm | parser

    try:
        result = chain.invoke({"question": question})
        result = normalize_query(result)

        result = {
            k: v for k, v in result.items()
            if v not in [None, "", "null"]
        }

        print(f"🔍 Final Query: {result}")
        return result

    except Exception as e:
        print(f"❌ Query extraction error: {e}")
        return {}


# =========================
# 3. RAG RETRIEVAL
# =========================
def retrieve_from_vector_db(user_question):

    if _vector_db is None:
        return None

    docs = _vector_db.max_marginal_relevance_search(
        user_question,
        k=RAG_TOP_K,
        fetch_k=RAG_FETCH_K
    )

    if not docs:
        return None

    return "\n\n".join(doc.page_content for doc in docs)