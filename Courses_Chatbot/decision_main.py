import streamlit as st
import langchain_helper as lch
import ugrad_vs_grad_decision as dh
import textwrap

st.title("Carnegie Mellon Course Recommender")

with st.sidebar:
    with st.form(key="my_form"):
        query = st.sidebar.text_area(
            label = "What are your academic interests?",
            max_chars=100,
            key="query"
        )

        submit_button = st.form_submit_button(label='Submit')

if query and submit_button:
    response = dh.get_question_type(query)
    st.subheader("Answer: ")
    repo = '<p style="font-family:sans-serif; color:Black; font-size: 20px;">' + response + '</p>'
    st.markdown(repo, unsafe_allow_html=True)