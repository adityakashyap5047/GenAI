import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMChain, LLMMathChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent
from langchain.callbacks import StreamlitCallbackHandler

### Set up the streamlit app
st.set_page_config(page_title="MathsGPT", page_icon="🦜")
st.title("🦜 MathsGPT: Your Personal Math Assistant")

groq_api_key = st.sidebar.text_input("Enter your Groq API Key", type="password")

if not groq_api_key:
    st.warning("Please enter your Groq API Key to use the app.")
    st.stop()

llm = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

### Initializing the tools
wikipedia_wrapper = WikipediaAPIWrapper()
wikipedia_tool = Tool(
    name="Wikipedia",
    func=wikipedia_wrapper.run,
    description="A Tool for searching the Internet to find the various information on the topics mentioned"
)

### Initializing the MATH Tool

math_chain = LLMMathChain.from_llm(llm=llm)

calculator = Tool(
    name="Calculator",
    func=math_chain.run,
    description="A Tool for answering math related questions. Only input mathematical expressions need to be provided."
)

prompt = """

You are an agent for solving users mathematical questions. Logically arrives the solution and provide a detiled explanation and display it point wise for the question below
Question: {question}
Answer:
"""

prompt_template = PromptTemplate(
    input_variables=["question"],
    template=prompt
)

### Combine all the tools into chain
chain = LLMChain(llm=llm, prompt=prompt_template)

reasoning_tool = Tool(
    name="Reasoning tool",
    func=chain.run,
    description="A Tool for answering logic-based and reasoning questions."
)

### Initialize the agent
assistant_agent = initialize_agent(
    tools=[wikipedia_tool, calculator, reasoning_tool],
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True,
)

