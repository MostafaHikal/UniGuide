from app.router import router
from app.retrieval import retrieve_from_vector_db
from app.responder import generate_response


# =========================
# CORE PIPELINE
# =========================
def chat_pipeline(question: str, session_id: str = "default", mode: str = "rag"):

    router_output = router(question=question, mode=mode)
    intent        = router_output.get("intent")

    context = None
    if intent == "rag":
        context = retrieve_from_vector_db(question)

    return generate_response(
        router_output=router_output,
        question=question,
        context=context,
    )


# =========================
# TEST
# =========================
if __name__ == "__main__":
    print(chat_pipeline("امتحان قضايا مجتمعية امتى؟"))