# RAG Complaint Bot
A smart and interactive grievance assistant built using **FastAPI, LangChain, OpenRouter LLMs, and Streamlit UI**. This chatbot helps users register complaints and track their status using **Retrieval-Augmented Generation (RAG)** and a vector database backed by FAISS.

📖 Getting Started
1.Clone the repo:
  git clone https://github.com/your-username/rag-complaint-bot.git

2. Install dependencies:
  pip install -r requirements.txt

3. Set your .env with OpenRouter key

4.Run FastAPI backend:
   uvicorn api.main:app --reload

5. Run Streamlit UI:
  streamlit run app.py


**Features**
✅ Complaint registration with validation
📱 Track complaint status using mobile number or complaint ID
🧠 LLM-powered assistant (Grok-1 via OpenRouter)
🔎 RAG-based contextual answers from uploaded PDF knowledge base
🗃️ SQLite for complaint storage
📊 Interactive UI built with Streamlit
🔁 Reset chat anytime with one click
🚀 Lightweight and beginner-friendly setup

**Tech Stack:**
_Backend_: FastAPI
_Frontend/UI_: Streamlit
_Database_: SQLite
_Vector Store_: FAISS
_LLM Provider_: OpenRouter (grok-3-beta)
_RAG Framework_: LangChain
_Embeddings_: OpenAIEmbeddings


