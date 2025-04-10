import streamlit as st
import pdfplumber
from docx import Document
from bs4 import BeautifulSoup
import requests

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

from transformers import pipeline
from langchain.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA

# Load static files

def extract_pdf_text(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


def extract_docx_text(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip() != ""])


def scrape_website(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text(separator=' ', strip=True)
    return ""


@st.cache_resource
def setup_rag():
    scraped_text = scrape_website("https://www.angelone.in/support")
    scraped_text += extract_pdf_text("file1.pdf")
    scraped_text += extract_pdf_text("file2.pdf")
    scraped_text += extract_pdf_text("file3.pdf")
    scraped_text += extract_pdf_text("file4.pdf")
    scraped_text += extract_docx_text("document.docx")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    documents = splitter.create_documents([scraped_text])

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(documents, embedding_model)
    pipe = pipeline("text2text-generation",
                    model="google/flan-t5-base", max_length=256)
    llm = HuggingFacePipeline(pipeline=pipe)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)


# UI
st.title("📚 Pretrained RAG Chatbot")

qa_chain = setup_rag()
query = st.text_input("Ask a question about the documents:")
if query:
    with st.spinner("Thinking..."):
        result = qa_chain(query)
        sources = result.get("source_documents", [])
        if not sources or len(" ".join([s.page_content for s in sources]).strip()) < 10:
            st.write("🤷‍♂️ I don't know.")
        else:
            st.markdown("**Answer:**")
            st.write(result["result"])
