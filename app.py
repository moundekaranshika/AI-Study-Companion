# import streamlit as st
# from PyPDF2 import PdfReader
# from utils import generate_summary, generate_questions, generate_flashcards, chat_with_notes
# st.markdown("""
# <style>
# .stButton button {
#     background-color: #4CAF50;
#     color: white;
#     border-radius: 10px;
#     height: 3em;
#     width: 100%;
# }
# </style>
# """, unsafe_allow_html=True)
# st.set_page_config(page_title="AI Study Companion", layout="wide")

# # 🌟 Title
# st.markdown("<h1 style='text-align: center;'>📚 AI Study Companion</h1>", unsafe_allow_html=True)
# st.markdown("<p style='text-align: center;'>Turn your notes into summaries, questions & flashcards instantly 🚀</p>", unsafe_allow_html=True)

# # 📂 Sidebar
# st.sidebar.title("⚙️ Settings")
# mode = st.sidebar.selectbox("Select Mode", ["Normal", "Explain Like I'm 5"])
# difficulty = st.sidebar.selectbox("Difficulty", ["Easy", "Medium", "Hard"])

# uploaded_file = st.file_uploader("📄 Upload your notes (PDF)", type="pdf")

# text = ""

# if uploaded_file:
#     reader = PdfReader(uploaded_file)
#     for page in reader.pages:
#         text += page.extract_text()

#     st.success("✅ Notes uploaded successfully!")

#     # 🔥 Tabs UI
#     tab1, tab2, tab3, tab4 = st.tabs(["📝 Summary", "🎤 Viva Questions", "🧠 Flashcards", "💬 Chat"])

#     with tab1:
#         if st.button("Generate Summary"):
#             with st.spinner("Generating summary..."):
#                 summary = generate_summary(text)
#                 st.markdown("### 📝 Summary")
#                 st.info(summary)

#     with tab2:
#         if st.button("Generate Questions"):
#             with st.spinner("Generating questions..."):
#                 questions = generate_questions(text)
#                 st.markdown("### 🎤 Viva Questions")
#                 st.success(questions)

#     with tab3:
#         if st.button("Generate Flashcards"):
#             with st.spinner("Generating flashcards..."):
#                 flashcards = generate_flashcards(text)
#                 st.markdown("### 🧠 Flashcards")
#                 st.warning(flashcards)
    
#     with tab4:
#         st.markdown("### 💬 Chat with your Notes")

#         if "chat_history" not in st.session_state:
#             st.session_state.chat_history = []

#         user_input = st.text_input("Ask anything from your notes:")

#         if st.button("Ask"):
#             if user_input:
#                 with st.spinner("Thinking..."):
#                     response = chat_with_notes(text, user_input)

#                     st.session_state.chat_history.append(("You", user_input))
#                     st.session_state.chat_history.append(("AI", response))

#         # Display chat
#         for role, msg in st.session_state.chat_history:
#             if role == "You":
#                 st.markdown(f"**🧑 You:** {msg}")
#             else:
#                 st.markdown(f"**🤖 AI:** {msg}")

# else:
#     st.info("👆 Upload a PDF to get started")

# import streamlit as st
# from PyPDF2 import PdfReader
# from pdf2image import convert_from_bytes
# import pytesseract
# from PIL import Image
# from export_utils import create_pdf
# from utils import generate_summary, generate_questions, generate_flashcards, chat_with_notes

# # Page config
# st.set_page_config(page_title="AI Study Companion", layout="wide")

# # 🎨 Custom Styling
# st.markdown("""
# <style>
# .stButton button {
#     background-color: #4CAF50;
#     color: white;
#     border-radius: 10px;
#     height: 3em;
#     width: 100%;
# }
# </style>
# """, unsafe_allow_html=True)

# # 🌟 Title
# st.markdown("<h1 style='text-align: center;'>📚 AI Study Companion</h1>", unsafe_allow_html=True)
# st.markdown("<p style='text-align: center;'>Turn your notes into summaries, questions & flashcards instantly 🚀</p>", unsafe_allow_html=True)

# # 📂 Sidebar
# st.sidebar.title("⚙️ Settings")
# mode = st.sidebar.selectbox("Select Mode", ["Normal", "Explain Like I'm 5"])
# difficulty = st.sidebar.selectbox("Difficulty", ["Easy", "Medium", "Hard"])

# # 📄 PDF Upload
# uploaded_file = st.file_uploader("Upload your notes (PDF)", type="pdf")


# 🧠 PDF Extraction Function (WITH OCR)
# def extract_text_from_pdf(uploaded_file):
#     text = ""

#     # Try normal extraction
#     try:
#         reader = PdfReader(uploaded_file)
#         for page in reader.pages:
#             extracted = page.extract_text()
#             if extracted:
#                 text += extracted
#     except:
#         pass

#     # If text too small → OCR
#     if len(text.strip()) < 100:
#         images = convert_from_bytes(uploaded_file.read())
#         for img in images:
#             text += pytesseract.image_to_string(img)

#     return text
# def extract_text_from_pdf(uploaded_file):
#     text = ""

#     # STEP 1: Try normal extraction
#     try:
#         uploaded_file.seek(0)
#         reader = PdfReader(uploaded_file)
#         for page in reader.pages:
#             extracted = page.extract_text()
#             if extracted:
#                 text += extracted
#     except:
#         pass

#     # STEP 2: If text too small → try OCR via pdf2image
#     if len(text.strip()) < 100:
#         try:
#             uploaded_file.seek(0)
#             images = convert_from_bytes(uploaded_file.read())
#             for img in images:
#                 text += pytesseract.image_to_string(img)
#         except Exception as e:
#             print("pdf2image failed:", e)

#     # STEP 3: FINAL fallback (ultra robust)
#     if len(text.strip()) < 100:
#         try:
#             uploaded_file.seek(0)
#             image = Image.open(uploaded_file)
#             text += pytesseract.image_to_string(image)
#         except Exception as e:
#             print("Final OCR fallback failed:", e)

#     return text

# import fitz  # PyMuPDF
# import streamlit as st

# @st.cache_data(show_spinner=False)
# def extract_text_from_pdf(uploaded_file):
#     text = ""

#     # 🥇 STEP 1: Fast extraction using PyMuPDF
#     try:
#         uploaded_file.seek(0)
#         pdf_bytes = uploaded_file.read()
#         doc = fitz.open(stream=pdf_bytes, filetype="pdf")

#         for page in doc[:5]:  # 🔥 limit to first 5 pages (FAST)
#             text += page.get_text()

#         if len(text.strip()) > 200:
#             return text

#     except Exception as e:
#         print("PyMuPDF failed:", e)

#     # 🥈 STEP 2: OCR (optimized)
#     try:
#         uploaded_file.seek(0)
#         images = convert_from_bytes(
#             uploaded_file.read(),
#             dpi=150,              # 🔥 lower DPI (faster)
#             first_page=1,
#             last_page=5           # 🔥 limit pages
#         )

#         for img in images:
#             text += pytesseract.image_to_string(
#                 img,
#                 config='--oem 3 --psm 6'   # 🔥 optimized OCR
#             )

#         if len(text.strip()) > 100:
#             return text

#     except Exception as e:
#         print("OCR failed:", e)

#     return text


# # 🚀 Main Logic
# text = ""

# if uploaded_file:
#     text = extract_text_from_pdf(uploaded_file)

#     st.success("✅ Notes uploaded and processed!")

#     st.write(f"📄 Extracted {len(text)} characters")

#     # 🔥 Tabs
#     tab1, tab2, tab3, tab4 = st.tabs([
#         "📝 Summary",
#         "🎤 Viva Questions",
#         "🧠 Flashcards",
#         "💬 Chat"
#     ])

#     # 📝 SUMMARY
#     with tab1:
#         if st.button("Generate Summary"):
#             with st.spinner("Generating summary..."):
#                 summary = generate_summary(text)
#                 st.markdown("### 📝 Summary")
#                 st.info(summary)

#     # 🎤 QUESTIONS
#     with tab2:
#         if st.button("Generate Questions"):
#             with st.spinner("Generating questions..."):
#                 questions = generate_questions(text)
#                 st.markdown("### 🎤 Viva Questions")
#                 st.success(questions)

#     # 🧠 FLASHCARDS
#     with tab3:
#         if st.button("Generate Flashcards"):
#             with st.spinner("Generating flashcards..."):
#                 flashcards = generate_flashcards(text)
#                 st.markdown("### 🧠 Flashcards")
#                 st.warning(flashcards)

#     # 💬 CHAT (ChatGPT Style)
#     with tab4:
#         st.markdown("### 💬 Chat with your Notes")

#         if "chat_history" not in st.session_state:
#             st.session_state.chat_history = []

#         # Display chat messages
#         for role, msg in st.session_state.chat_history:
#             if role == "user":
#                 st.markdown(f"""
#                 <div style='text-align: right; margin: 10px;'>
#                     <span style='background-color:#DCF8C6; padding:10px 15px; border-radius:15px; display:inline-block;'>
#                         {msg}
#                     </span>
#                 </div>
#                 """, unsafe_allow_html=True)
#             else:
#                 st.markdown(f"""
#                 <div style='text-align: left; margin: 10px;'>
#                     <span style='background-color:#F1F0F0; padding:10px 15px; border-radius:15px; display:inline-block;'>
#                         {msg}
#                     </span>
#                 </div>
#                 """, unsafe_allow_html=True)

#         # Chat input
#         user_input = st.chat_input("Ask anything from your notes...")

#         if user_input:
#             st.session_state.chat_history.append(("user", user_input))

#             with st.spinner("Thinking..."):
#                 response = chat_with_notes(text, user_input)

#             st.session_state.chat_history.append(("ai", response))

#             st.rerun()

# else:
#     st.info("👆 Upload a PDF to get started")

# import streamlit as st
# import fitz  # PyMuPDF
# from pdf2image import convert_from_bytes
# import pytesseract
# from PIL import Image
# import os

# from utils import generate_summary, generate_questions, generate_flashcards, chat_with_notes
# from export_utils import create_pdf

# # Page config
# st.set_page_config(page_title="AI Study Companion", layout="wide")

# # 🎨 Styling
# st.markdown("""
# <style>
# .stButton button {
#     background-color: #4CAF50;
#     color: white;
#     border-radius: 10px;
#     height: 3em;
#     width: 100%;
# }
# </style>
# """, unsafe_allow_html=True)

# # 🌟 Title
# st.markdown("<h1 style='text-align: center;'>📚 AI Study Companion</h1>", unsafe_allow_html=True)
# st.markdown("<p style='text-align: center;'>Turn your notes into summaries, questions & flashcards instantly 🚀</p>", unsafe_allow_html=True)

# # 📂 Sidebar
# st.sidebar.title("⚙️ Settings")
# mode = st.sidebar.selectbox("Mode", ["Normal", "Explain Like I'm 5"])
# difficulty = st.sidebar.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
# fast_mode = st.sidebar.checkbox("⚡ Fast Mode (first 5 pages)", value=True)

# # 📄 Upload
# uploaded_file = st.file_uploader("Upload your notes (PDF)", type="pdf")

# # 🧠 Session state
# if "summary" not in st.session_state:
#     st.session_state.summary = ""

# if "questions" not in st.session_state:
#     st.session_state.questions = ""

# if "flashcards" not in st.session_state:
#     st.session_state.flashcards = ""

# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# # 🚀 FAST + ROBUST PDF Extraction
# @st.cache_data(show_spinner=False)
# def extract_text_from_pdf(uploaded_file, fast_mode=True):
#     text = ""
#     pages_to_read = 5 if fast_mode else 20

#     # 🥇 PyMuPDF (fast)
#     try:
#         uploaded_file.seek(0)
#         pdf_bytes = uploaded_file.read()
#         doc = fitz.open(stream=pdf_bytes, filetype="pdf")

#         for page in doc[:pages_to_read]:
#             text += page.get_text()

#         if len(text.strip()) > 200:
#             return text

#     except Exception as e:
#         print("PyMuPDF failed:", e)

#     # 🥈 OCR via pdf2image
#     try:
#         uploaded_file.seek(0)
#         images = convert_from_bytes(
#             uploaded_file.read(),
#             dpi=150,
#             first_page=1,
#             last_page=pages_to_read
#         )

#         for img in images:
#             text += pytesseract.image_to_string(
#                 img,
#                 config='--oem 3 --psm 6'
#             )

#         if len(text.strip()) > 100:
#             return text

#     except Exception as e:
#         print("OCR failed:", e)

#     # 🥉 Final fallback
#     try:
#         uploaded_file.seek(0)
#         image = Image.open(uploaded_file)
#         text += pytesseract.image_to_string(image)
#     except Exception as e:
#         print("Final fallback failed:", e)

#     return text


# # 🔥 MAIN APP
# if uploaded_file:
#     text = extract_text_from_pdf(uploaded_file, fast_mode)

#     if len(text.strip()) == 0:
#         st.error("❌ Could not extract text from this file.")
#     else:
#         st.success("✅ Notes processed successfully!")
#         st.write(f"📄 Extracted {len(text)} characters")

#         # Tabs
#         tab1, tab2, tab3, tab4 = st.tabs([
#             "📝 Summary",
#             "🎤 Viva Questions",
#             "🧠 Flashcards",
#             "💬 Chat"
#         ])

#         # 📝 Summary
#         with tab1:
#             if st.button("Generate Summary"):
#                 with st.spinner("Generating summary..."):
#                     st.session_state.summary = generate_summary(text)
#                     st.info(st.session_state.summary)

#         # 🎤 Questions
#         with tab2:
#             if st.button("Generate Questions"):
#                 with st.spinner("Generating questions..."):
#                     st.session_state.questions = generate_questions(text)
#                     st.success(st.session_state.questions)

#         # 🧠 Flashcards
#         with tab3:
#             if st.button("Generate Flashcards"):
#                 with st.spinner("Generating flashcards..."):
#                     st.session_state.flashcards = generate_flashcards(text)
#                     st.warning(st.session_state.flashcards)

#         # 💬 Chat
#         with tab4:
#             st.markdown("### 💬 Chat with your Notes")

#             for role, msg in st.session_state.chat_history:
#                 if role == "user":
#                     st.markdown(f"""
#                     <div style='text-align: right; margin: 10px;'>
#                         <span style='background-color:#DCF8C6; padding:10px 15px; border-radius:15px;'>
#                             {msg}
#                         </span>
#                     </div>
#                     """, unsafe_allow_html=True)
#                 else:
#                     st.markdown(f"""
#                     <div style='text-align: left; margin: 10px;'>
#                         <span style='background-color:#F1F0F0; padding:10px 15px; border-radius:15px;'>
#                             {msg}
#                         </span>
#                     </div>
#                     """, unsafe_allow_html=True)

#             user_input = st.chat_input("Ask anything from your notes...")

#             if user_input:
#                 st.session_state.chat_history.append(("user", user_input))

#                 with st.spinner("Thinking..."):
#                     response = chat_with_notes(text, user_input)

#                 st.session_state.chat_history.append(("ai", response))
#                 st.rerun()

#         # 📄 EXPORT PDF
#         if st.session_state.summary or st.session_state.questions or st.session_state.flashcards:

#             st.markdown("---")
#             if st.button("📄 Export to PDF"):
#                 file_path = create_pdf(
#                     st.session_state.summary,
#                     st.session_state.questions,
#                     st.session_state.flashcards
#                 )

#                 with open(file_path, "rb") as f:
#                     st.download_button(
#                         label="⬇️ Download PDF",
#                         data=f,
#                         file_name="study_notes.pdf",
#                         mime="application/pdf"
#                     )

# else:
#     st.info("👆 Upload a PDF to get started")

# import streamlit as st
# import fitz
# from pdf2image import convert_from_bytes
# import pytesseract
# from PIL import Image

# from utils import generate_summary, generate_questions, generate_flashcards, chat_with_notes
# from export_utils import create_pdf

# # Page config
# st.set_page_config(page_title="AI Study Companion", layout="wide")

# # 🎨 PREMIUM UI STYLING
# st.markdown("""
# <style>
# .block-container {
#     padding-top: 2rem;
# }

# /* Cards */
# .card {
#     background: #ffffff;
#     padding: 20px;
#     border-radius: 15px;
#     box-shadow: 0px 4px 20px rgba(0,0,0,0.08);
#     margin-bottom: 20px;
# }

# /* Buttons */
# .stButton button {
#     background: linear-gradient(135deg, #667eea, #764ba2);
#     color: white;
#     border-radius: 10px;
#     height: 3em;
#     font-weight: bold;
# }

# /* Chat bubbles */
# .user-bubble {
#     background-color: #6366f1;
#     color: white;
#     padding: 10px 15px;
#     border-radius: 15px;
#     display: inline-block;
# }

# .ai-bubble {
#     background-color: #e5e7eb;
#     padding: 10px 15px;
#     border-radius: 15px;
#     display: inline-block;
# }
# </style>
# """, unsafe_allow_html=True)

# # 🌟 HEADER
# st.markdown("""
# <div style='text-align:center; padding:20px'>
#     <h1> AI Study Companion</h1>
#     <p style='color:gray; font-size:18px'>
#         Turn boring notes into smart summaries, flashcards & AI chat
#     </p>
# </div>
# """, unsafe_allow_html=True)

# # 🔥 FEATURE ROW
# col1, col2, col3 = st.columns(3)
# with col1:
#     st.markdown("###  Smart Summary")
# with col2:
#     st.markdown("###  Viva Prep")
# with col3:
#     st.markdown("###  AI Chat")

# # 📂 SIDEBAR
# st.sidebar.title("Settings")
# fast_mode = st.sidebar.checkbox("Fast Mode", value=True)

# # 📄 FILE UPLOAD
# uploaded_file = st.file_uploader("Upload your notes (PDF)", type="pdf")

# # 🧠 SESSION STATE
# if "summary" not in st.session_state:
#     st.session_state.summary = ""

# if "questions" not in st.session_state:
#     st.session_state.questions = ""

# if "flashcards" not in st.session_state:
#     st.session_state.flashcards = ""

# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# # 🚀 FAST + ROBUST EXTRACTION
# @st.cache_data(show_spinner=False)
# def extract_text_from_pdf(uploaded_file, fast_mode=True):
#     text = ""
#     pages_to_read = 5 if fast_mode else 20

#     # PyMuPDF
#     try:
#         uploaded_file.seek(0)
#         doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")

#         for page in doc[:pages_to_read]:
#             text += page.get_text()

#         if len(text.strip()) > 200:
#             return text

#     except:
#         pass

#     # OCR
#     try:
#         uploaded_file.seek(0)
#         images = convert_from_bytes(
#             uploaded_file.read(),
#             dpi=150,
#             first_page=1,
#             last_page=pages_to_read
#         )

#         for img in images:
#             text += pytesseract.image_to_string(img, config='--oem 3 --psm 6')

#         if len(text.strip()) > 100:
#             return text

#     except:
#         pass

#     # Final fallback
#     try:
#         uploaded_file.seek(0)
#         image = Image.open(uploaded_file)
#         text += pytesseract.image_to_string(image)
#     except:
#         pass

#     return text


# # 🚀 MAIN APP
# if uploaded_file:
#     text = extract_text_from_pdf(uploaded_file, fast_mode)

#     if len(text.strip()) == 0:
#         st.error(" Could not extract text from this file.")
#     else:
#         st.success(" Notes processed successfully!")

#         tab1, tab2, tab3, tab4 = st.tabs([
#             " Summary",
#             " Questions",
#             " Flashcards",
#             " Chat"
#         ])

#         # SUMMARY
#         with tab1:
#             if st.button("Generate Summary"):
#                 with st.spinner("Generating..."):
#                     st.session_state.summary = generate_summary(text)

#             if st.session_state.summary:
#                 st.markdown(f"""
#                 <div class="card">
#                 <h4> Summary</h4>
#                 <p>{st.session_state.summary}</p>
#                 </div>
#                 """, unsafe_allow_html=True)

#         # QUESTIONS
#         with tab2:
#             if st.button("Generate Questions"):
#                 with st.spinner("Generating..."):
#                     st.session_state.questions = generate_questions(text)

#             if st.session_state.questions:
#                 st.markdown(f"""
#                 <div class="card">
#                 <h4> Viva Questions</h4>
#                 <p>{st.session_state.questions}</p>
#                 </div>
#                 """, unsafe_allow_html=True)

#         # FLASHCARDS
#         with tab3:
#             if st.button("Generate Flashcards"):
#                 with st.spinner("Generating..."):
#                     st.session_state.flashcards = generate_flashcards(text)

#             if st.session_state.flashcards:
#                 st.markdown(f"""
#                 <div class="card">
#                 <h4>Flashcards</h4>
#                 <p>{st.session_state.flashcards}</p>
#                 </div>
#                 """, unsafe_allow_html=True)

#         # CHAT
#         with tab4:
#             st.markdown("### Chat with your Notes")

#             for role, msg in st.session_state.chat_history:
#                 if role == "user":
#                     st.markdown(f"""
#                     <div style='text-align:right; margin:10px'>
#                         <div class="user-bubble">{msg}</div>
#                     </div>
#                     """, unsafe_allow_html=True)
#                 else:
#                     st.markdown(f"""
#                     <div style='text-align:left; margin:10px'>
#                         <div class="ai-bubble">{msg}</div>
#                     </div>
#                     """, unsafe_allow_html=True)

#             user_input = st.chat_input("Ask anything from your notes...")

#             if user_input:
#                 st.session_state.chat_history.append(("user", user_input))

#                 with st.spinner("Thinking..."):
#                     response = chat_with_notes(text, user_input)

#                 st.session_state.chat_history.append(("ai", response))
#                 st.rerun()

#         # EXPORT
#         if st.session_state.summary or st.session_state.questions or st.session_state.flashcards:
#             st.markdown("---")
#             if st.button(" Export to PDF"):
#                 file_path = create_pdf(
#                     st.session_state.summary,
#                     st.session_state.questions,
#                     st.session_state.flashcards
#                 )

#                 with open(file_path, "rb") as f:
#                     st.download_button(
#                         " Download PDF",
#                         f,
#                         "study_notes.pdf",
#                         "application/pdf"
#                     )

# else:
#     st.info("👆 Upload a PDF to get started")

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