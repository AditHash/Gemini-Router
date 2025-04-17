# # ✅ MCP Server 4 – RAG (Docs + Gemini Flash 1.5)

import os
import tempfile
from fastapi import FastAPI, UploadFile
# from langchain.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import PyMuPDFLoader
# from langchain.vectorstores import FAISS
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from fastapi.middleware.cors import CORSMiddleware

# Set Google API key
os.environ["GOOGLE_API_KEY"] = os.environ.get("GEMINI_API_KEY")

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from the frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📌 Initialize models
embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Global variable to hold the FAISS vector store in memory
vectorstore = None

@app.post("/upload")
async def upload_pdf(file: UploadFile):
    global vectorstore

    # Save uploaded file to temp location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    # 📄 Load PDF using LangChain loader
    loader = PyMuPDFLoader(tmp_path)
    documents = loader.load()

    # 📚 Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(documents)

    # 🧠 Create or extend FAISS vector store
    if vectorstore is None:
        vectorstore = FAISS.from_documents(chunks, embedding=embedding_model)
    else:
        vectorstore.add_documents(chunks)

    return {"status": "uploaded", "chunks": len(chunks)}


@app.post("/query")
async def query_rag(q: dict):
    global vectorstore
    question = q["question"]

    if vectorstore is None:
        return {"error": "No documents uploaded yet."}

    # 🔎 Setup QA chain with FAISS retriever
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever()
    )

    answer = qa_chain.run(question)
    return {"answer": answer}
