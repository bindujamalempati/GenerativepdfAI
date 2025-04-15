# AskMyDoc – Document Q&A App (LLM + FAISS)

AskMyDoc is a simple LLM-powered document Q&A system that allows users to query their documents using semantic search and vector similarity. It uses a FAISS index to store document embeddings and respond with relevant context.

## 📦 Features
- Upload documents and ask questions interactively
- Uses FAISS for fast similarity search
- LLM integration (e.g., OpenAI, HuggingFace models)

## 📁 Files
- `app.py` – Streamlit app code
- `document_qa.ipynb` – Jupyter notebook for testing/document understanding
- `faiss_index/` – Contains FAISS and pickle files (not tracked by Git)
- `.env` – Environment variables (excluded from repo)

## 🚀 How to Run
1. Clone the repo
2. Create `.env` file with your API keys
3. Run the app:

```bash
streamlit run app.py
