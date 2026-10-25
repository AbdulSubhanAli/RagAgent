# RAG Agent - Upload ANY Document and ask questions about it
# Abdul Subhan - Universal Document RAG

import os
import tempfile
import streamlit as st

from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ui.theme import apply_aurora_theme
from ui.components import (
    render_header,
    render_empty_state,
    render_indexed_pill,
    render_user_message,
    render_assistant_message,
    render_thinking,
    render_indexing_progress,
    render_error,
    render_no_sources,
    render_3d_source_stack
)

# Page Setup
st.set_page_config(
    page_title="Abdul Subhan - Ask Your Knowledge",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_aurora_theme()

# Session version tracker to force hard-resets on input widgets
if "login_id" not in st.session_state:
    st.session_state.login_id = 0

# Sidebar
with st.sidebar:
    st.markdown("<h2 class='sidebar-title'>Settings</h2>", unsafe_allow_html=True)
    
    # Dynamic widget key forces Streamlit to instantiate a clean, empty input box on logout
    api_key_widget_key = f"api_key_input_{st.session_state.login_id}"
    api_key = st.text_input("OpenAI API Key", type="password", key=api_key_widget_key)
    
    model_name = st.selectbox("Chat model", ["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini"], key="model_select")
    chunk_size = st.slider("Chunk size", 500, 2000, 1000, step=100, key="chunk_size_slider")
    chunk_overlap = st.slider("Chunk overlap", 0, 400, 150, step=50, key="chunk_overlap_slider")
    top_k = st.slider("Retrieved chunks (k)", 2, 10, 4, key="top_k_slider")

    # Logout button ONLY appears when an API key is actively entered
    if api_key:
        st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
        if st.button("🚪 Logout", key="logout_btn", use_container_width=True):
            # 1. Purge environment memory
            os.environ.pop("OPENAI_API_KEY", None)
            
            # 2. Increment session version ID
            new_login_id = st.session_state.login_id + 1
            
            # 3. Clear all cached session state and assign new version
            st.session_state.clear()
            st.session_state.login_id = new_login_id
            
            # 4. Rerun app
            st.rerun()

# Halt execution if no API key is provided
if not api_key:
    st.info("Enter your OpenAI API key in the sidebar to begin.")
    st.stop()

os.environ["OPENAI_API_KEY"] = api_key

render_header()

SUPPORTED_EXTENSIONS = ["pdf", "docx", "doc", "txt", "md", "csv", "pptx", "html", "json", "py", "log"]

uploaded_doc = st.file_uploader(
    "Upload a document (PDF, Word, Text, CSV, PPTX, HTML, Code, etc.)", 
    type=SUPPORTED_EXTENSIONS, 
    key="doc_uploader"
)

def load_document_from_bytes(file_bytes: bytes, filename: str) -> list[Document]:
    ext = os.path.splitext(filename)[1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        if ext == ".pdf":
            return PyPDFLoader(tmp_path).load()
        elif ext == ".csv":
            try:
                return CSVLoader(tmp_path, encoding="utf-8").load()
            except Exception:
                return CSVLoader(tmp_path, encoding="latin-1").load()
        elif ext in [".docx", ".doc"]:
            try:
                from langchain_community.document_loaders import Docx2txtLoader
                return Docx2txtLoader(tmp_path).load()
            except Exception:
                with open(tmp_path, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
                return [Document(page_content=text, metadata={"page": 1, "source": filename})]
        elif ext == ".pptx":
            try:
                from langchain_community.document_loaders import UnstructuredPowerPointLoader
                return UnstructuredPowerPointLoader(tmp_path).load()
            except Exception:
                with open(tmp_path, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
                return [Document(page_content=text, metadata={"page": 1, "source": filename})]
        else:
            try:
                return TextLoader(tmp_path, encoding="utf-8").load()
            except Exception:
                with open(tmp_path, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
                return [Document(page_content=text, metadata={"page": 1, "source": filename})]
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

def build_vectorstore(file_bytes: bytes, filename: str, size: int, overlap: int) -> FAISS:
    docs = load_document_from_bytes(file_bytes, filename)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return FAISS.from_documents(chunks, embeddings)

if uploaded_doc is not None:
    file_sig = (uploaded_doc.name, uploaded_doc.size, chunk_size, chunk_overlap)
    if st.session_state.get("file_sig") != file_sig:
        render_indexing_progress()
        try:
            st.session_state.vectorstore = build_vectorstore(
                uploaded_doc.getvalue(), uploaded_doc.name, chunk_size, chunk_overlap
            )
            st.session_state.file_sig = file_sig
            st.session_state.messages = []
            st.session_state.latest_retrieved_docs = []
        except Exception as e:
            render_error(f"Error indexing document: {str(e)}")
            st.stop()
    
    render_indexed_pill(uploaded_doc.name)

RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are a helpful assistant that answers questions strictly using the "
     "provided context from a document.\n"
     "Rules:\n"
     "1. Answer ONLY from the context below.\n"
     "2. If the answer is not in the context, say: \"I couldn't find that in the document.\"\n"
     "3. Cite the page/section or source location if available, e.g. (p. 3).\n\n"
     "Context:\n{context}"),
    ("human", "{question}"),
])

def format_docs(docs) -> str:
    formatted = []
    for d in docs:
        page_val = d.metadata.get('page', d.metadata.get('row', '?'))
        if isinstance(page_val, int):
            page_val += 1
        formatted.append(f"[Page/Ref {page_val}]\n{d.page_content}")
    return "\n\n".join(formatted)

def get_chain(vectorstore: FAISS, model: str, k: int):
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    llm = ChatOpenAI(model=model, temperature=0)
    return (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | RAG_PROMPT
        | llm
        | StrOutputParser()
    ), retriever

if "vectorstore" in st.session_state:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "latest_retrieved_docs" not in st.session_state:
        st.session_state.latest_retrieved_docs = []

    has_pending_user_msg = (
        len(st.session_state.messages) > 0 
        and st.session_state.messages[-1]["role"] == "user"
    )

    chat_col, stack_col = st.columns([1.3, 1], gap="small")

    with chat_col:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                render_user_message(msg["content"])
            elif msg["role"] == "assistant":
                render_assistant_message(msg["content"], msg.get("sources", []))

        if has_pending_user_msg:
            pending_question = st.session_state.messages[-1]["content"]

            chain, retriever = get_chain(
                st.session_state.vectorstore, model_name, top_k
            )

            thinking_placeholder = st.empty()
            with thinking_placeholder.container():
                render_thinking()

            try:
                retrieved_docs = retriever.invoke(pending_question)
                
                sources_list = []
                for idx, doc in enumerate(retrieved_docs):
                    page_val = doc.metadata.get("page", doc.metadata.get("row", "?"))
                    if isinstance(page_val, int):
                        page_val += 1
                    sources_list.append({
                        "doc_name": uploaded_doc.name if uploaded_doc else "document",
                        "page": page_val,
                        "snippet": doc.page_content,
                        "score": doc.metadata.get("score", None)
                    })
                
                st.session_state.latest_retrieved_docs = sources_list
                
                answer_chunks = []
                answer_placeholder = st.empty()
                
                for chunk in chain.stream(pending_question):
                    answer_chunks.append(chunk)
                    current_text = "".join(answer_chunks)
                    thinking_placeholder.empty()
                    with answer_placeholder.container():
                        render_assistant_message(current_text, sources_list)
                
                full_answer = "".join(answer_chunks)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": full_answer,
                    "sources": sources_list
                })
                st.rerun()

            except Exception as e:
                thinking_placeholder.empty()
                render_error(f"Failed to generate answer: {str(e)}")

        question = st.chat_input("Ask a question about the document...", key="chat_input")
        if question:
            st.session_state.messages.append({"role": "user", "content": question})
            st.rerun()

    with stack_col:
        st.markdown("<div style='color: #5CF0DA; font-size: 12px; letter-spacing: 2px; font-weight: 700; margin-bottom: 16px; text-transform: uppercase;'>RETRIEVED SOURCES</div>", unsafe_allow_html=True)
        if st.session_state.latest_retrieved_docs:
            render_3d_source_stack(st.session_state.latest_retrieved_docs)
        else:
            render_no_sources()
else:
    render_empty_state()