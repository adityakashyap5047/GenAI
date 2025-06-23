import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq

st.set_page_config(page_title="LangChain: Chat with SQL DB", page_icon="🦜")
st.title("🦜 LangChain: Chat with SQL DB")

LOCALDB = 'USE_LOCAL_DB'
MYSQL = 'USE_MYSQL_DB'

radio_opt = ["Use SQLITE 3 DATABASE - STUDENT.db", "Connect to your own SQL Database"]

selected_opt = st.radio(label="Choose a DB which you want to chat", options=radio_opt)

if radio_opt.index(selected_opt) == 1:
    db_uri = MYSQL
    mysql_host = st.sidebar.text_input("Provide MySQL Host")
    mysql_user = st.sidebar.text_input("Provide MySQL User")
    mysql_password = st.sidebar.text_input("Provide MySQL Password", type="password")
    mysql_db = st.sidebar.text_input("Provide MySQL Database Name")
else:
    db_uri = LOCALDB

api_key = st.sidebar.text_input("Enter your Groq API Key", type="password")

if not db_uri:
    st.info("Please enter the database information and uri")

if not api_key:
    st.info("Please enter your Groq API Key")

### LLM Model
llm = ChatGroq(groq_api_key=api_key, model="Llama3-8b-8192", streaming=True)

@st.cache_resource(ttl="2h")
def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
    if db_uri == LOCALDB:
        db_file_path = (Path(__file__).parent/"student.db").absolute()
        print(f"Using local SQLite database at {db_file_path}")
        creator = lambda: sqlite3.connect(f"file: {db_file_path}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    elif db_uri == MYSQL:
        if not all([mysql_host, mysql_user, mysql_password, mysql_db]):
            st.error("Please provide all MySQL connection details.")
            st.stop()
            return None
        mysql_uri = f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"
        print(f"Connecting to MySQL database at {mysql_uri}")
        return SQLDatabase(create_engine(mysql_uri))