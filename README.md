
# 📚 Generative PDF AI

> AI-powered assistant for interactive PDF exploration — ask questions, summarize content, and search contextually across documents.

---

## 🚀 Features

- 🔍 **Question Answering**: Ask natural language questions on PDFs.  
- 📑 **Summarization**: Extract key insights from lengthy documents.  
- ⚡ **Semantic Search**: Uses embeddings for contextual lookup.  
- 🧠 **LLM Integration**: Powered by HuggingFace + LangChain.  
- 🗂 **Vector Database**: Efficient retrieval using FAISS / pgvector.  

---

## 🛠 Tech Stack

- **Core**: Python  
- **LLM Frameworks**: LangChain, HuggingFace  
- **Vector DBs**: FAISS, pgvector  
- **Other**: PyPDF2, NumPy, Pandas  

---

## 📦 Setup & Installation

```bash
git clone https://github.com/bindujamalempati/GenerativepdfAI.git
cd GenerativepdfAI
pip install -r requirements.txt
Add .env with:

ini
Copy code
OPENAI_API_KEY=your_openai_key
HUGGINGFACE_API_KEY=your_hf_key
🎯 Usage
bash
Copy code
python app.py --pdf path/to/file.pdf
Example query:

vbnet
Copy code
Enter your question: "Summarize section 3"
Answer: "Section 3 discusses …"
📊 Example Flow
Upload PDF

System splits into chunks → embeddings

Query is vectorized → matched context

LLM generates final answer

📄 License
MIT License.
