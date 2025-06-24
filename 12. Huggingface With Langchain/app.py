import validators
import streamlit as st

from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader
from langchain_huggingface import HuggingFaceEndpoint

### Streamlit app configuration
st.set_page_config(page_title="LangChain: Text Summarization", page_icon="🦜")
st.title("🦜 LangChain: Summarized Text")


### Get the Hugging Face API key and url(YT or website) to be summarized
with st.sidebar:
    hf_api_key = st.text_input("Enter your Hugging Face API Key", type="password")

repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
llm = HuggingFaceEndpoint(repo_id=repo_id, max_new_tokens=150, temperature=0.7, huggingfacehub_api_token=hf_api_key, task="text-generation")

### Prompt Template
prompt_template = """

Provide a summary of the following content in 300 words:
Content: {text}

"""

prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

generic_url = st.text_input("Enter the YouTube URL or Website URL to be summarized", label_visibility="collapsed")

if st.button("Summarize the Content from YT or Website"):
    ### Validate all the inputs
    if not hf_api_key.strip() or not generic_url.strip():
        st.error("Please Provide the necessary information")
    elif not validators.url(generic_url):
        st.error("Please Provide a valid URL")
    else:
        try:
            with st.spinner("Waiting..."):
                ## loading the website or yt content
                if "youtube.com" in generic_url or "youtu.be" in generic_url:
                    loader = YoutubeLoader.from_youtube_url(generic_url, add_video_info=False)
                else:
                    loader = UnstructuredURLLoader(urls=[generic_url], ssl_verify=False,
                                                   headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
                docs = loader.load()

                ### Summarizing the content
                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                summary = chain.run(docs)

                st.success(summary)
        except Exception as e:
            st.error(f"An error occurred: {e}")