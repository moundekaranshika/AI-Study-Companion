import streamlit as st
import fitz
from pdf2image import convert_from_bytes
from io import BytesIO

from utils import (
    generate_summary,
    generate_questions,
    generate_flashcards,
    chat_with_notes,
    ocr_space_api
)
from export_utils import create_pdf

st.set_page_config(page_title="AI Study Companion", layout="wide")

# 🎨 DARK MODE SAFE UI
st.markdown("""
<style>
.card {
    background: var(--background-color);
    color: var(--text-color);
    padding: 20px;
    border-radius: 15px;
    border: 1px solid rgba(128,128,128,0.2);
    margin-bottom: 20px;
}
.stButton button {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border-radius: 10px;
}
.user-bubble {
    background-color: #6366f1;
    color: white;
    padding: 10px;
    border-radius: 15px;
}
.ai-bubble {
    background-color: rgba(200,200,200,0.2);
    padding: 10px;
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("<h1 style='text-align:center;'> AI Study Companion</h1>", unsafe_allow_html=True)

# SIDEBAR
fast_mode = st.sidebar.checkbox(" Fast Mode", value=True)

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

# SESSION STATE
for key in ["summary", "questions", "flashcards"]:
    if key not in st.session_state:
        st.session_state[key] = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 🔥 EXTRACTION FUNCTION
@st.cache_data(show_spinner=False)
def extract_text(uploaded_file, fast_mode=True):
    text = ""
    pages = 5 if fast_mode else 15

    # PyMuPDF
    try:
        uploaded_file.seek(0)
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in doc[:pages]:
            text += page.get_text()
        if len(text.strip()) > 200:
            return text
    except:
        pass

    # OCR via API
    try:
        uploaded_file.seek(0)
        images = convert_from_bytes(
            uploaded_file.read(),
            dpi=200,
            first_page=1,
            last_page=pages
        )

        for img in images:
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            text += ocr_space_api(buffer.getvalue())

        return text
    except:
        return text


# MAIN
if uploaded_file:
    text = extract_text(uploaded_file, fast_mode)

    if len(text.strip()) == 0:
        st.warning("Could not extract text. Try another file.")
        manual = st.text_area(" Paste notes manually")
        if manual:
            text = manual

    if text:
        tabs = st.tabs(["Summary", "Questions", "Flashcards", "Chat"])

        with tabs[0]:
            if st.button("Generate Summary"):
                st.session_state.summary = generate_summary(text)

            if st.session_state.summary:
                st.markdown(f"<div class='card'><pre>{st.session_state.summary}</pre></div>", unsafe_allow_html=True)

        with tabs[1]:
            if st.button("Generate Questions"):
                st.session_state.questions = generate_questions(text)

            if st.session_state.questions:
                st.markdown(f"<div class='card'><pre>{st.session_state.questions}</pre></div>", unsafe_allow_html=True)

        with tabs[2]:
            if st.button("Generate Flashcards"):
                st.session_state.flashcards = generate_flashcards(text)

            if st.session_state.flashcards:
                st.markdown(f"<div class='card'><pre>{st.session_state.flashcards}</pre></div>", unsafe_allow_html=True)

        with tabs[3]:
            for role, msg in st.session_state.chat_history:
                style = "user-bubble" if role == "user" else "ai-bubble"
                align = "right" if role == "user" else "left"
                st.markdown(f"<div style='text-align:{align}'><div class='{style}'>{msg}</div></div>", unsafe_allow_html=True)

            user_input = st.chat_input("Ask anything...")

            if user_input:
                st.session_state.chat_history.append(("user", user_input))
                response = chat_with_notes(text, user_input)
                st.session_state.chat_history.append(("ai", response))
                st.rerun()

        # EXPORT
        if st.session_state.summary or st.session_state.questions:
            if st.button("📄 Export PDF"):
                file = create_pdf(
                    st.session_state.summary,
                    st.session_state.questions,
                    st.session_state.flashcards
                )
                with open(file, "rb") as f:
                    st.download_button("Download PDF", f, "notes.pdf")

else:
    st.info("Upload a PDF to begin")
