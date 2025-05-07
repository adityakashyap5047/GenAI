from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama

import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

### Langchain Tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "GENAI - APP With Ollama"

### Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please response to the user queries"),
        ("user", "Question: {question}"),
    ]
)

def generate_response(question, llm = "gemma:2b"):
    llm = Ollama(model=llm)
    parser = StrOutputParser()
    chain = prompt | llm | parser
    answer = chain.invoke({"question": question})
    return answer


### Title of the app
st.title("Enhanced Q&A Chatbot")

### Main interface for user input
st.write("## Ask your question")
question = st.text_input("Enter your question here")

if question:
    response = generate_response(question)
    st.write(response)
else:
    st.write("Please enter a question to get a response.")