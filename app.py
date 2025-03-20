import streamlit as st
from summarize import load_text, summarize_text, send_summary
import os

st.title("Summarizer Bot")

with st.sidebar:
    with st.form(key='my_form'):
        url = st.sidebar.text_area(
            label="What is the URL?",
            max_chars=250
            )
        number = st.sidebar.text_input(
            label="What is the phone number?",
            max_chars=250,
            type = "password"
            )

if url:
    docs = load_text(url)
    response = summarize_text(docs)
    response = response["output_text"]
    st.write(response)

    if number:
      send_summary(response, number)

