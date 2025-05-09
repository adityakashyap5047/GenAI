### RAG Q&A Conversation with PDF Including Chat History

import streamlit as st
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

import os
from dotenv import load_dotenv
load_dotenv()

os.environ['HF_TOKEN'] = os.getenv('HF_TOKEN')
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLm-L6-v2")

### Setup the streamlit
st.title("RAG Q&A Conversation with PDF Including Chat History")
st.write("Upload Pdf's and chat with their content")

### Input the Groq API key
groq_api_key = st.text_input("Enter your Groq API key", type="password")

### Check if the API key is provided
if groq_api_key:
    llm = ChatGroq(groq_api_key=groq_api_key, model="Gemma2-9b-It")

    session_id = st.text_input("Session ID", value="default_session")

    