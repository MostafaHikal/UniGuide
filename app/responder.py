import json
from langchain_groq import ChatGroq
from app.prompts import STRUCTURED_PROMPT, RAG_PROMPT, GENERAL_PROMPT
from app.config import MODEL_NAME, GROQ_API_KEY


llm = ChatGroq(
    temperature=0,
    model_name=MODEL_NAME,
    groq_api_key=GROQ_API_KEY,
)


# =========================
# SAFE FORMATTER
# =========================
def safe_json(data: dict):
    if not data:
        return {}

    hidden_fields = ["type"]

    return {
        k: v
        for k, v in data.items()
        if v is not None and k not in hidden_fields
    }


# =========================
# MAIN FUNCTION
# =========================
def generate_response(router_output, question, context=None, student_context=""):

    intent = router_output.get("intent")
    data   = router_output.get("data")

    try:

        # -------------------------
        # UNKNOWN
        # -------------------------
        if intent == "unknown":
            chain = GENERAL_PROMPT | llm
            res = chain.invoke({
                "message": question,
                "student_context": student_context
            })
            return res.content.strip()

        # -------------------------
        # STRUCTURED
        # -------------------------
        elif intent == "structured":

            if not data:
                return "ممكن توضح سؤالك أكتر؟"

            status = data.get("status")

            if status == "not_found":
                return "مش لاقي بيانات مطابقة للسؤال، ممكن تحدده أكتر؟"

            if status == "error":
                return "مش قادر أفهم السؤال، ممكن تعيد صياغته؟"

            if status == "found":

                results = data.get("results", [])

                cleaned_results = [
                    safe_json(record)
                    for record in results
                ]

                chain = STRUCTURED_PROMPT | llm

                res = chain.invoke({
                    "question": question,
                    "data": json.dumps(
                        cleaned_results,
                        ensure_ascii=False,
                        indent=2
                    ),
                    "student_context": student_context
                })

                return res.content.strip()

        # -------------------------
        # RAG
        # -------------------------
        elif intent == "rag":

            if not context:
                return "مش لاقي معلومات كافية للإجابة على السؤال ده، حاول توضح أكتر."

            chain = RAG_PROMPT | llm

            res = chain.invoke({
                "question": question,
                "context": context,
                "student_context": student_context
            })

            return res.content.strip()

        # -------------------------
        # FALLBACK
        # -------------------------
        return "حدث خطأ غير متوقع، حاول مرة أخرى."

    except Exception as e:
        return f"⚠️ System Error: {str(e)}"