1. Library Imports
The app imports essential libraries for:

UI (streamlit)

PDF/DOCX parsing (pdfplumber, python-docx)

Web scraping (requests, BeautifulSoup)

LangChain components (text splitting, embedding, vector storage, LLM, QA chain)

Transformers (HuggingFacePipeline and FLAN-T5 model)

🔹 2. Text Extraction Functions
✅ extract_pdf_text(file_path)
Reads and extracts all text from each page of a PDF file using pdfplumber.

✅ extract_docx_text(file_path)
Reads a .docx file using python-docx, extracts non-empty paragraphs, and combines them into one string.

✅ scrape_website(url)
Sends a GET request to the specified website, parses the HTML, and extracts all visible text using BeautifulSoup.

📌 Purpose: These functions collect relevant data from various sources to form the knowledge base for the chatbot.

🔹 3. @st.cache_resource - setup_rag()
This function is the core setup logic that runs only once (cached):

✅ a. Data Collection
Concatenates all extracted content from:

The Angel One support webpage

Four PDF files: file1.pdf to file4.pdf

One DOCX file: document.docx

✅ b. Text Chunking
Uses LangChain's RecursiveCharacterTextSplitter to break the full text into smaller overlapping chunks:

chunk_size = 500

chunk_overlap = 50

📌 This improves semantic matching while preserving some context overlap.

✅ c. Embedding & FAISS Vector Store
Embeds all text chunks using HuggingFace’s "all-MiniLM-L6-v2" model

Stores the vectors in a FAISS vector store for fast semantic search

✅ d. Language Model (LLM) Setup
Uses a lightweight FLAN-T5 model (google/flan-t5-base) via transformers.pipeline to generate text from questions and context.

✅ e. RAG Chain Construction
Builds a RetrievalQA chain using LangChain:

Retrieves top 3 relevant documents from FAISS

Passes them with the user query to the FLAN-T5 model

Returns the generated answer + source documents

🔹 4. Streamlit User Interface
✅ a. st.title("📚 Pretrained RAG Chatbot")
Displays the title of the app.

✅ b. query = st.text_input(...)
Provides an input field where users can type their questions.

✅ c. When a user enters a question:
Shows a loading spinner with st.spinner("Thinking...")

Sends the question to the RAG chain
