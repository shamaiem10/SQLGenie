import streamlit as st
from langchain_helper import get_few_shot_db_chain

st.title("University Records Q&A")

question = st.text_input("Ask a question about student records:")

if question:
    chain = get_few_shot_db_chain()
    response = chain.run(question)
    st.header("Answer")
    st.write(response)