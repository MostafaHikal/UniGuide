from app.retrieval import (
    extract_query_from_question,
    filter_json_data
)


# =========================
# RESPONSE BUILDER
# =========================
def build_response(
    intent,
    status="ok",
    data=None,
    message=None
):

    return {
        "intent": intent,
        "status": status,
        "data": data,
        "message": message
    }


# =========================
# MAIN ROUTER
# =========================
def router(question, mode):

    intent = mode

    # =========================
    # STRUCTURED
    # =========================
    if intent == "structured":

        query = extract_query_from_question(
            question
        )

        if not query:

            return build_response(
                intent="structured",
                status="error",
                data={
                    "status": "error",
                    "results": []
                },
                message="Failed to extract query"
            )

        result = filter_json_data(query)

        return build_response(
            intent="structured",
            status=result["status"],
            data=result
        )

    # =========================
    # RAG
    # =========================
    elif intent == "rag":

        return build_response(
            intent="rag",
            status="ok",
            data=None
        )

    # =========================
    # FALLBACK
    # =========================
    return build_response(
        intent="unknown",
        status="error",
        data=None,
        message="Invalid mode"
    )