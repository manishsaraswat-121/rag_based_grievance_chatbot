from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter

def build_index():
    loader = PyPDFLoader(r"C:\Users\manis\OneDrive\Documents\rag-complaint-bot\knowledge_base\sample_faq.pdf")
    docs = loader.load()
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    FAISS.from_documents(chunks, embeddings).save_local("vectordb/faiss_index")

if __name__ == "__main__":
    build_index()