# 📄 GenerativepdfAI

**GenerativepdfAI** is an intelligent PDF Question-Answering web app built using `Streamlit`, enabling users to upload one or multiple PDF files, ask natural language questions, and receive precise answers powered by `OpenAI` and `LangChain`.

---

## 🚀 Features

- 📁 Upload one or more PDFs
- 💬 Ask questions in natural language
- 🧠 Get instant, AI-generated answers
- 📃 Chat history and session memory
- 📥 Export answers and summaries
- 🎙️ Voice-to-text query support (placeholder)
- 💡 Suggested questions for quick access
- 🧾 Feedback box for user input
- 🌓 Custom dark/light theme toggle
- ⚙️ Real-time animated spinner during response
- 🖼️ Custom logo and chatbot avatar

---

## 🧰 Tech Stack & Tools

| Area                | Technologies Used                                                                 |
|---------------------|------------------------------------------------------------------------------------|
| **Frontend**        | Streamlit, HTML (for injected styles), CSS animations                             |
| **Backend**         | Python, LangChain, OpenAI API, HuggingFace Transformers                           |
| **PDF Parsing**     | PyMuPDF (via `langchain_community.document_loaders`)                              |
| **Embeddings**      | HuggingFace Embeddings (`sentence-transformers/all-MiniLM-L6-v2`)                 |
| **Vector Store**    | FAISS (for semantic similarity search across document chunks)                     |
| **Environment**     | `.env` with `python-dotenv`                                                       |
| **Containerization**| Docker (local usage optional)                                                     |
| **Version Control** | Git, GitHub                                                                        |
| **Deployment**      | Streamlit Cloud ([Live App](https://GenerativepdfAI2.streamlit.app))                     |

---
