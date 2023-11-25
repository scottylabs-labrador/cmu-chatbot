from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.vectorstores import FAISS
import os
from dotenv import load_dotenv
from langchain.document_loaders import JSONLoader
import json
from pathlib import Path
from pprint import pprint
from langchain.document_loaders import PyPDFLoader
import pinecone
import openai

load_dotenv()

embeddings = OpenAIEmbeddings() # use embeddings from OpenAI

A = os.getenv("api_key")
B = os.getenv("environment")
C = os.getenv("O_AI_KEY")
D = os.getenv("index_name")

pinecone.init(api_key=A, environment=B)      
index = pinecone.Index(D)
openai.api_key = C

def get_vector_loaded_db():
    return FAISS.load_local("./", OpenAIEmbeddings(), "undergraduate_catalog")

def get_response_from_query(query, user_ugrad_grad, user_department, k=4):
    # What courses do you recommend?
    repo = openai.Embedding.create(input=query, model="text-embedding-ada-002")
    query_vector = repo["data"][0]["embedding"]
    if(user_ugrad_grad == ""):
        st_valid = "$ne"
    else:
        st_valid = "$eq"
    if(user_department == ""):
        dept_valid = "$ne"
    else:
        dept_valid = "$eq"

    docs_page_content = index.query(
    vector=query_vector,
    filter={
        "student_type": {st_valid: user_ugrad_grad},
        "department": {dept_valid: user_department}
    },
    top_k=k,
    include_metadata=True
    )

    llm = OpenAI(model="gpt-3.5-turbo-instruct") # Use gpt-3.5-turbo-instruct for great responses at preferable prices
    prompt = PromptTemplate(
        input_variables=["question", "docs"],
        template = """
        You are a helpful Course Recommendation assistant that can recommend courses based on their description.  
        Answer the following question: {question} 
        By searching the following Carnegie Mellon courses: {docs}

        Only use the factual information from the course descriptions to answer the question.set
        Include the course number and title of the course that you recommend. 

        Your answer should only include courses that are directly relevant to the question and be detailed. Include at most 1 courses in your response. Use proper punctuation.

        If you feel like you don't have enough information to answer the question, say "I don't know".
        """,
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run(question=query, docs=docs_page_content)
    response = response.replace("\n", "")
    return response