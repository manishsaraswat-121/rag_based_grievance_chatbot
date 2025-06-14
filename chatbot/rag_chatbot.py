import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

load_dotenv()
VSTORE_PATH = "vectordb/faiss_index"

def load_vectorstore():
    return FAISS.load_local(
        VSTORE_PATH,
        HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"),
        allow_dangerous_deserialization=True
    )

def query_rag(query: str) -> str:
    vs = load_vectorstore()
    llm = ChatOpenAI(
        openai_api_base="https://openrouter.ai/api/v1",
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        model="mistralai/mistral-7b-instruct",
        temperature=0.2
    )
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vs.as_retriever()
    )
    result = qa.run(query)
    print("\n📦 RAG Response:", result)
    return result

'''if __name__ == "__main__":
    query = "How can I file a complaint using the chatbot?"
    answer = query_rag(query)
    print("\nFinal Answer:\n", answer)'''

