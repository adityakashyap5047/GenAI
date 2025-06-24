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

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hello! I am MathsGPT, your personal math assistant. Who can answer your math-related questions"}
    ]

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

### Lets start the interaction
question = st.text_area("Enter your question:", "I have 5 bananas and 7 grapes. I eat 2 bananas and give away 3 grapes. Then I buy a dozen apples and 2 packs of blueberries contain 25 barries. How many total fruits do I have at end?")

if st.button("find my answer"):
    if question:
        with st.spinner("Generating response..."):
            st.session_state["messages"].append({"role": "user", "content": question})
            st.chat_message("user").write(question)

            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            response = assistant_agent.run(st.session_state["messages"], callbacks=[st_cb])

            st.session_state["messages"].append({"role": "assistant", "content": response})
            st.write('### Response:')
            st.write(response)

    else:
        st.warning("Please enter a question to get an answer.")