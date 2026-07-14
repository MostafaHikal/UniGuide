import gradio as gr
import uuid
import os
from app.main import chat_pipeline
from app.ingestion import ingest


# =========================
# Chat Handler
# الـ Gradio 6 بيمرر history كـ list of dicts
# =========================
def chat_handler(message, history, session_id, mode):
    if not message.strip():
        return "", history

    # رسالة ترحيب في أول message
    if not history:
        history = [{"role": "assistant", "content": "أهلاً! أنا CampusMind، مساعدك الجامعي. اسألني عن أي حاجة 😊"}]

    response = chat_pipeline(message, session_id=session_id, mode=mode)

    history.append({"role": "user",      "content": message})
    history.append({"role": "assistant", "content": response})

    return "", history


# =========================
# Upload Handler
# =========================
def upload_handler(file):
    if file is None:
        return "⚠️ اختر ملف الأول."

    ext = os.path.splitext(file.name)[-1].lower()
    if ext not in [".pdf", ".jpg", ".jpeg", ".png"]:
        return "❌ نوع الملف مش مدعوم. ارفع PDF أو صورة."

    try:
        result = ingest(file.name)
        return f"✅ تم بنجاح: {result}"
    except Exception as e:
        return f"❌ خطأ: {str(e)}"


# =========================
# UI
# =========================
with gr.Blocks(title="CampusMind") as demo:

    gr.Markdown("# 🎓 CampusMind")
    gr.Markdown("مساعدك الجامعي الذكي — اسأل عن الجداول والامتحانات ولوائح الكلية")

    session_id = gr.State(lambda: str(uuid.uuid4()))

    with gr.Tabs():

        # ===== TAB 1: Chat =====
        with gr.TabItem("💬 Chat"):

            mode_selector = gr.Radio(
            choices=[
                ("📅 Schedules & Exams", "structured"),
                ("🏛️ College Information", "rag")
            ],
            value="structured",
            label="Search Mode"
)

            chatbot = gr.Chatbot(label="CampusMind", height=450)

            msg_input = gr.Textbox(
                label="سؤالك",
                placeholder="مثال: امتحان الماث امتى؟",
                lines=2
            )

            send_btn = gr.Button("إرسال", variant="primary")

            send_btn.click(
                fn=chat_handler,
                inputs=[msg_input, chatbot, session_id, mode_selector],
                outputs=[msg_input, chatbot]
            )

            msg_input.submit(
                fn=chat_handler,
                inputs=[msg_input, chatbot, session_id, mode_selector],
                outputs=[msg_input, chatbot]
            )

        # ===== TAB 2: Upload =====
        with gr.TabItem("📂 رفع ملفات"):

            gr.Markdown("### ارفع ملف PDF أو صورة لإضافته للنظام")
            gr.Markdown("الـ PDF ← معلومات الكلية | الصور ← جداول وامتحانات")

            file_input    = gr.File(label="اختر ملف", file_types=[".pdf", ".jpg", ".jpeg", ".png"])
            upload_btn    = gr.Button("🚀 رفع وتحليل", variant="primary")
            upload_status = gr.Markdown("*في انتظار الملف*")

            upload_btn.click(
                fn=upload_handler,
                inputs=file_input,
                outputs=upload_status
            )


# =========================
# RUN
# =========================
if __name__ == "__main__":
    demo.launch()