import validators
import streamlit as st

from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader

### Streamlit app configuration
st.set_page_config(page_title="LangChain: Text Summarization", page_icon="🦜")
st.title("🦜 LangChain: Summarized Text")


### Get the Groq API key and url(YT or website) to be summarized
with st.sidebar:
    groq_api_key = st.text_input("Enter your Groq API Key", type="password")


generic_url = st.text_input("Enter the YouTube URL or Website URL to be summarized", label_visibility="collapsed")

if st.button("Summarize the Content from YT or Website"):
    ### Validate all the inputs
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please Provide the necessary information")
    elif not validators.url(generic_url):
        st.error("Please Provide a valid URL")
    else:
        try:
            with st.spinner("Waiting..."):
                ## loading the website or yt content
                if "youtube.com" in generic_url or "youtu.be" in generic_url:
                    loader = YoutubeLoader.from_youtube_url(generic_url, add_video_info=True)
                else:
                    loader = UnstructuredURLLoader(urls=[generic_url], ssl_verify=False,
                                                   headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
                data = loader.load()