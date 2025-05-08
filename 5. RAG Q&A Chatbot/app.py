import streamlit as st
import os

from langchain_groq import ChatGroq
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS  
from langchain_community.document_loaders import PyPDFDirectoryLoader

from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

gorq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(groq_api_key=gorq_api_key, model="Gemma-7b-It")

prompt = ChatPromptTemplate.from_template(
    """

        Answer the question based on the provided context only.
        Please provide the most accurate response based on the question
        <context>
            {context}
        </context>

        Question: {input}

    """
)

def create_vector_embedding():
    if "vecotrs" not in st.session_state:
        st.session_state.embeddings = OllamaEmbeddings(model="gemma:2b")
        st.session_state.loader = PyPDFDirectoryLoader("Research Paper")
        st.session_state.docs = st.session_state.loader.load()
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        st.session_state.split_docs = st.session_state.text_splitter.split_documents(st.session_state.docs[: 50])
        st.session_state.vectorstore = FAISS.from_documents(st.session_state.split_docs, st.session_state.embeddings)

prompt = st.text_input("Enter your question from the Research Paper: ")

if st.button("Submit"):
    create_vector_embedding()
    st.write("Vector Database is ready")

import time

if prompt:
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = st.session_state.vectorstore.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    start = time.process_time()
    response = retrieval_chain.invoke({"input": prompt})

    print(f"Response time: {time.process_time() - start} seconds")

    st.write(response["answer"])

    