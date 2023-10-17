import streamlit as st
import langchain_helper as lch
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

if query:
    db = lch.get_vector_loaded_db()
    response = lch.get_response_from_query(db, query)
    #docs = response = lch.get_response_from_query(db, query)
    st.subheader("Answer: ")
    st.text(textwrap.fill(response, width = 80))