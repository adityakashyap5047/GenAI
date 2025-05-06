from fastapi import FastAPI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

from langserve import add_routes

import os
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

model = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

### Prompt Template ###
generic_template = "Translate the following into {language}: "

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", generic_template),
        ("user", "{text}")
    ],
)

### Output Parser ###
parser = StrOutputParser()

### Creating the chain ###
chain = prompt | model | parser

### App definition ###
app = FastAPI(
    title="LangServe - Groq",
    version="1.0",
    description="A simple API server using Langchain runnable interface"
)

### Adding chain routes ###
add_routes(
    app,
    chain,
    path="/chain"
)

### Running the app ###
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)