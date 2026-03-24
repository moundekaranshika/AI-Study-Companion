import streamlit as st
import fitz
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image

from utils import generate_summary, generate_questions, generate_flashcards, chat_with_notes
from export_utils import create_pdf

# Page config
st.set_page_config(page_title="AI Study Companion", layout="wide")

# 🎨 THEME-SAFE STYLING (FIXED DARK MODE)
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}

/* Adaptive card */
.card {
    background: var(--background-color);
    color: var(--text-color);
    padding: 20px;
    border-radius: 15px;
    border: 1px solid rgba(128,128,128,0.2);
    box-shadow: 0px 4px 20px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

/* Buttons */
.stButton button {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border-radius: 10px;
    height: 3em;
    font-weight: bold;
}

/* Chat bubbles */
.user-bubble {
    background-color: #6366f1;
    color: white;
    padding: 10px 15px;
    border-radius: 15px;
}

.ai-bubble {
    background-color: rgba(200,200,200,0.2);
    color: inherit;
    padding: 10px 15px;
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

# 🌟 HEADER
st.markdown("""
<div style='text-align:center; padding:20px'>
    <h1> AI Study Companion</h1>
    <p style='font-size:18px; opacity:0.7'>
        Turn your notes into smart summaries, flashcards & AI chat
    </p>
</div>
""", unsafe_allow_html=True)

# 🔥 FEATURES
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### Smart Summary")
with col2:
    st.markdown("### Viva Prep")
with col3:
    st.markdown("###  AI Chat")

# 📂 SIDEBAR
st.sidebar.title(" Settings")
fast_mode = st.sidebar.checkbox(" Fast Mode", value=True)

# 📄 UPLOAD
uploaded_file = st.file_uploader("Upload your notes (PDF)", type="pdf")

# 🧠 SESSION STATE
for key in ["summary", "questions", "flashcards"]:
    if key not in st.session_state:
        st.session_state[key] = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 🚀 FAST + ROBUST EXTRACTION
@st.cache_data(show_spinner=False)
def extract_text_from_pdf(uploaded_file, fast_mode=True):
    text = ""
    pages_to_read = 5 if fast_mode else 20

    # PyMuPDF
    try:
        uploaded_file.seek(0)
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in doc[:pages_to_read]:
            text += page.get_text()
        if len(text.strip()) > 200:
            return text
    except:
        pass

    # OCR
    try:
        uploaded_file.seek(0)
        images = convert_from_bytes(
            uploaded_file.read(),
            dpi=150,
            first_page=1,
            last_page=pages_to_read
        )
        for img in images:
            text += pytesseract.image_to_string(img, config='--oem 3 --psm 6')
        if len(text.strip()) > 100:
            return text
    except:
        pass

    # Final fallback
    try:
        uploaded_file.seek(0)
        image = Image.open(uploaded_file)
        text += pytesseract.image_to_string(image)
    except:
        pass

    return text

# 🚀 MAIN
if uploaded_file:
    text = extract_text_from_pdf(uploaded_file, fast_mode)

    if len(text.strip()) == 0:
        st.error(" Could not extract text from this file.")
    else:
        st.success("Notes processed successfully!")

        tab1, tab2, tab3, tab4 = st.tabs([
            "Summary",
            "Questions",
            "Flashcards",
            "Chat"
        ])

        # SUMMARY
        with tab1:
            if st.button("Generate Summary"):
                with st.spinner("Generating..."):
                    st.session_state.summary = generate_summary(text)

            if st.session_state.summary:
                st.markdown(f"""
                <div class="card">
                <h4>Summary</h4>
                <pre style="white-space: pre-wrap;">{st.session_state.summary}</pre>
                </div>
                """, unsafe_allow_html=True)

        # QUESTIONS
        with tab2:
            if st.button("Generate Questions"):
                with st.spinner("Generating..."):
                    st.session_state.questions = generate_questions(text)

            if st.session_state.questions:
                st.markdown(f"""
                <div class="card">
                <h4>🎤 Viva Questions</h4>
                <pre style="white-space: pre-wrap;">{st.session_state.questions}</pre>
                </div>
                """, unsafe_allow_html=True)

        # FLASHCARDS
        with tab3:
            if st.button("Generate Flashcards"):
                with st.spinner("Generating..."):
                    st.session_state.flashcards = generate_flashcards(text)

            if st.session_state.flashcards:
                st.markdown(f"""
                <div class="card">
                <h4> Flashcards</h4>
                <pre style="white-space: pre-wrap;">{st.session_state.flashcards}</pre>
                </div>
                """, unsafe_allow_html=True)

        # CHAT
        with tab4:
            st.markdown("###  Chat with your Notes")

            for role, msg in st.session_state.chat_history:
                if role == "user":
                    st.markdown(f"""
                    <div style='text-align:right; margin:10px'>
                        <div class="user-bubble">{msg}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='text-align:left; margin:10px'>
                        <div class="ai-bubble">{msg}</div>
                    </div>
                    """, unsafe_allow_html=True)

            user_input = st.chat_input("Ask anything from your notes...")

            if user_input:
                st.session_state.chat_history.append(("user", user_input))

                with st.spinner("Thinking..."):
                    response = chat_with_notes(text, user_input)

                st.session_state.chat_history.append(("ai", response))
                st.rerun()

        # EXPORT PDF
        if st.session_state.summary or st.session_state.questions or st.session_state.flashcards:
            st.markdown("---")
            if st.button(" Export to PDF"):
                file_path = create_pdf(
                    st.session_state.summary,
                    st.session_state.questions,
                    st.session_state.flashcards
                )

                with open(file_path, "rb") as f:
                    st.download_button(
                        "⬇ Download PDF",
                        f,
                        "study_notes.pdf",
                        "application/pdf"
                    )

else:
    st.info("👆 Upload a PDF to get started")
