import requests
import streamlit as st

language = [
  "Hindi",
  "French",
  "English",
  "Spanish",
  "German",
  "Italian",
  "Portuguese",
  "Dutch",
  "Russian",
  "Chinese",
  "Japanese",
  "Korean",
  "Arabic",
]


def get_groq_response(input_language, input_text):
    json_body={
      "input": {
        "language": input_language,
        "text": input_text
      },
      "config": {},
      "kwargs": {}
    }
    response=requests.post("http://127.0.0.1:8000/chain/invoke", json=json_body)

    print(response.json())


    return response.json().get("output")

## Streamlit app
st.title("Language Translator Using LCEL")
input_language = st.selectbox("Select the language you want to convert to", language)
input_text = st.text_input("Enter the text you want to convert:-")

if input_text:
  st.write(get_groq_response(input_language, input_text))