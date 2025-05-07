import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv

load_dotenv()

### Langchain Tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")

### Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please response to the user queries"),
        ("user", "Question: {question}"),
    ]
)

def generate_response(question, api_key, llm, temperature, max_tokens):
    openai.api_key = api_key
    llm = ChatOpenAI(model=llm, temperature=temperature, max_tokens=max_tokens)
    parser = StrOutputParser()
    chain = prompt | llm | parser
    answer = chain.invoke({"question": question})
    return answer

### Title of the app
st.title("Enhanced Q&A Chatbot")
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

### Drop down for LLM selection
llm = st.sidebar.selectbox(
    "Select the LLM model",
    ("gpt-4o", "gpt-4-turbo", "gpt-4"),
)

### Slider for temperature and max tokens
temperature = st.sidebar.slider("Select the temperature", min_value=0.0, max_value=1.0, value=0.5)
max_tokens = st.sidebar.slider("Select the max tokens", min_value=50, max_value=300, value=150)

### Main interface for user input
st.write("## Ask your question")
question = st.text_input("Enter your question here")

if question:
    response = generate_response(question, api_key, llm, temperature, max_tokens)
    st.write(response)
else:
    st.write("Please enter a question to get a response.")