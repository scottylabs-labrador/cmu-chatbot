from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
from langchain.document_loaders import JSONLoader
import json
from pathlib import Path
from pprint import pprint
from langchain.document_loaders import PyPDFLoader

load_dotenv()

embeddings = OpenAIEmbeddings()
'''
def create_vector_db_from_json() -> FAISS:
    loader = JSONLoader(
    file_path='./courses.json',
    jq_schema='.',
    text_content=False)

    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size= 1000, chunk_overlap=100)
    docs = text_splitter.split_documents(data)
    db = FAISS.from_documents(docs, embeddings)
    return db
'''#Do not use the function above it is very computationally expensive, instead used pre-embedded database used by get_vector_laoded_db().

'''
def create_vector_db_from_pdf() -> FAISS:
    loader = PyPDFLoader("2022-2023-Catalog.pdf")

    pages = loader.load_and_split()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size= 2000, chunk_overlap=50)
    docs = text_splitter.split_documents(pages)
    db = FAISS.from_documents(pages, embeddings)
    db.save_local("./", "undergraduate_catalog")
    return db
    ''' #Do not use this function because it is computationally expensive, instead use pre-embedded database.


def get_vector_loaded_db():
    return FAISS.load_local("./", OpenAIEmbeddings(), "undergraduate_catalog")

def get_response_from_query(db, query, k=2):#Changed k to 2 from 4 while using ugrad catalog as datasource.
    # text-davinci can hand 4097 tokens
    #What courses do you reccomend?
    docs = db.similarity_search(query, k=k)
    docs_page_content = " ".join([d.page_content for d in docs])
    llm = OpenAI(model="gpt-3.5-turbo-instruct")
    #Use gpt-3.5-turbo-instruct for great responses at preferable prices
    prompt = PromptTemplate(
        input_variables=["question", "docs"],
        template = """
        You are a helpful Course Reccomendation assistant that can reccommend courses based on their description.  
        Answer the following question: {question} 
        By searching the following Carnegie Mellon courses: {docs}

        Only use the factual information from the course descriptions to answer the question.set
        Include the course number and title of courses that you recommend.
        If you feel like you don't have enough information to answer the question,
        say "I don't know".ImportError
        Your answer should only include courses that are directly relevant to the question and be detailed. Include at most 1 courses in your response.  Use proper punctuation.
        """,
    )
    chain = LLMChain(llm=llm, prompt = prompt)
    response = chain.run(question=query, docs = docs_page_content)
    response = response.replace("\n", "")
    return response

