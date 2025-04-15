import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from openai import OpenAI
import tempfile
from datetime import datetime
import base64

# --- Load environment variables ---
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Configure Streamlit page ---
st.set_page_config(page_title="AskMyDoc", layout="wide", page_icon="📄")

# --- Inject animated loading spinner CSS ---
st.markdown("""
    <style>
    .element-container:has(> .stMarkdown) { transition: all 0.5s ease-in-out; }
    .chat-avatar {
        width: 30px;
        margin-right: 10px;
        vertical-align: middle;
    }
    .spinner-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100px;
    }
    .loader {
        border: 8px solid #f3f3f3;
        border-top: 8px solid #3498db;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        animation: spin 1s linear infinite;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
""", unsafe_allow_html=True)

# --- Load Logo ---
logo_path = r"C:\\Users\\nisse\\Desktop\\askmydoc_logo.png"
logo = None
if os.path.exists(logo_path):
    try:
        logo = Image.open(logo_path)
    except Exception as e:
        st.warning("⚠️ Failed to load logo image.")

# --- Sidebar ---
with st.sidebar:
    if logo:
        st.image(logo, width=140)
    st.title("📄 AskMyDoc")
    st.markdown("""
    Welcome to **AskMyDoc** – your intelligent document assistant.

    Upload a PDF, ask questions, and get accurate answers instantly.
    """)
    st.markdown("---")
    st.markdown("👤 **Author:** Balaji Nissenkarao")
    st.markdown("🌐 [GitHub Repo](https://github.com/NBalaji0317/AskMyDoc)")
    st.markdown("---")
    feedback = st.text_area("💬 Have feedback or suggestions?", placeholder="Type your thoughts here...")
    if st.button("Submit Feedback"):
        st.success("✅ Thanks for your feedback!")

# --- Show logo above title (main page) ---
if logo:
    st.image(logo, width=200)

# --- Main Title ---
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <h1 style='font-size: 40px;'>📚 AskMyDoc</h1>
    <p style='font-size: 18px;'>Your AI-powered assistant for instant insights from PDFs</p>
</div>
""", unsafe_allow_html=True)

# --- Metrics Layout ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📄 Upload", "PDF Documents")
with col2:
    st.metric("💬 Ask", "Natural Questions")
with col3:
    st.metric("✅ Get", "Accurate Answers")

# --- File Uploader (Multi-doc support) ---
pdf_files = st.file_uploader("Upload one or more PDF documents", type=["pdf"], accept_multiple_files=True)

if pdf_files:
    all_chunks = []
    file_names = []

    for pdf_file in pdf_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(pdf_file.read())
            file_path = tmp.name
            file_names.append(pdf_file.name)

        loader = PyMuPDFLoader(file_path)
        documents = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(documents)
        all_chunks.extend(chunks)

    st.success(f"📄 Successfully processed: {', '.join(file_names)}")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(all_chunks, embeddings)

    st.markdown("### 🔍 Ask your documents anything:")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "saved_answers" not in st.session_state:
        st.session_state.saved_answers = []

    # Suggested Questions
    st.markdown("💡 Suggested Questions:")
    suggestions = ["What is the main topic?", "Summarize this document.", "Who is the author?", "List key points."]
    cols = st.columns(len(suggestions))
    for i, q in enumerate(suggestions):
        if cols[i].button(q):
            st.session_state.suggested_question = q

    # Voice-to-text input
    audio_input = st.file_uploader("🎙️ Record your question (WAV/MP3)", type=["wav", "mp3"])
    voice_text = ""
    if audio_input:
        st.audio(audio_input)
        st.info("Voice-to-text transcription will be available in future updates (placeholder text used).")
        voice_text = "(Transcribed) What are the highlights of this document?"

    question = st.text_input("Your Question", value=st.session_state.get("suggested_question", "") or voice_text)

    if question:
        docs = vectorstore.similarity_search(question, k=3)
        context = "\n\n".join([doc.page_content for doc in docs])

        with st.spinner("🤖 Thinking..."):
            spinner_html = """
            <div class="spinner-wrapper">
                <div class="loader"></div>
            </div>
            """
            spinner_placeholder = st.empty()
            spinner_placeholder.markdown(spinner_html, unsafe_allow_html=True)

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Answer using the provided context only."},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
                ]
            )
            spinner_placeholder.empty()

        answer = response.choices[0].message.content
        st.markdown("### 🧠 Answer:")
        st.markdown(f"<img src='https://cdn-icons-png.flaticon.com/512/4712/4712027.png' class='chat-avatar'> {answer}", unsafe_allow_html=True)

        st.session_state.chat_history.append((question, answer))
        st.session_state.saved_answers.append({"question": question, "answer": answer})

    if st.session_state.chat_history:
        st.markdown("---")
        st.markdown("### 📃 Chat History")
        for q, a in reversed(st.session_state.chat_history):
            st.markdown(f"**Q:** {q}")
            st.markdown(f"**A:** {a}")
            st.markdown("---")

        if st.button("📅 Download Chat Summary"):
            summary_text = "\n\n".join([f"Q: {entry['question']}\nA: {entry['answer']}" for entry in st.session_state.saved_answers])
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            summary_filename = f"AskMyDoc_Chat_{timestamp}.txt"
            with open(summary_filename, "w", encoding="utf-8") as f:
                f.write(summary_text)
            with open(summary_filename, "rb") as f:
                st.download_button(label="⬇️ Download Chat Summary", data=f, file_name=summary_filename, mime="text/plain")

# --- Footer ---
st.markdown("""
---
<div style='text-align: center;'>
    <small>Built with ❤️ by Balaji Nissenkarao | <a href='https://github.com/NBalaji0317/AskMyDoc' target='_blank'>GitHub</a></small>
</div>
""", unsafe_allow_html=True)
