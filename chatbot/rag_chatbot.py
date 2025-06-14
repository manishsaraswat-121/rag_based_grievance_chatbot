import os
from dotenv import load_dotenv
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

# Load environment variables
load_dotenv()

# Define path to vector store
VSTORE_PATH = "vectordb/faiss_index"

def load_vectorstore():
    """Load the local FAISS vector store."""
    return FAISS.load_local(VSTORE_PATH, OpenAIEmbeddings())

async def query_rag(query: str) -> str:
    """
    Handle queries via Retrieval Augmented Generation using Grok (via OpenRouter).
    """
    vs = load_vectorstore()
    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(
            openai_api_base="https://openrouter.ai/api/v1",
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),
            model="openrouter/xai/grok-1",
            temperature=0.2
        ),
        chain_type="stuff",
        retriever=vs.as_retriever()
    )
    return qa.run(query)
