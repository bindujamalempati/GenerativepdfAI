import streamlit as st
import os
from dotenv import load_dotenv
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from openai import OpenAI
import tempfile

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

st.set_page_config(page_title="📄 GenAI PDF Q&A Bot", layout="centered")
st.title("📄 Ask Your PDF - Powered by OpenRouter 🤖")

pdf_file = st.file_uploader("Upload your PDF", type=["pdf"])

if pdf_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_file.read())
        file_path = tmp.name

    st.success("📄 PDF uploaded successfully!")

    loader = PyMuPDFLoader(file_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    question = st.text_input("💬 Ask a question from the document:")
    
    if question:
        docs = vectorstore.similarity_search(question, k=3)
        context = "\n\n".join([doc.page_content for doc in docs])

        with st.spinner("🤖 Thinking..."):
            response = client.chat.completions.create(
                model="mistralai/mixtral-8x7b-instruct",
                messages=[
                    {"role": "system", "content": "Answer using the provided context only."},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
                ]
            )
            answer = response.choices[0].message.content
            st.markdown("### 🧠 Answer:")
            st.write(answer)


# & "C:\Users\nisse\genai_env\Scripts\streamlit.exe" run "C:\Users\nisse\Desktop\MyStuff\GenAI_QA_Bot\app.py"


