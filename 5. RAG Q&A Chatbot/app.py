import streamlit as st
import os

from langchain_groq import ChatGroq
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS  
from langchain_community.document_loaders import PypdfLoader

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

