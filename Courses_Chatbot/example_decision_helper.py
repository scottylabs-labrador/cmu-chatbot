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

def get_question_type(query):
    llm = OpenAI(model="gpt-3.5-turbo-instruct")
    #gpt-3.5-turbo-instruct
    #Use gpt-3.5-turbo-instruct for great responses at preferable prices
    prompt = PromptTemplate(
        input_variables=["question"],
        template = """
        You are a question type assistant, who categorizes questions into specific catagories.
        Based on the following question: "{question}" 

        If the question is related to dining respond with one word "dining", If the question is related to courses respond with one word "courses"
        Only use the factual information from the question.set to answer make your determination.
        You may use your internal intuition to make judgements, including biased ones if it will help with your interpretation work.
        If you feel like you don't have enough information to answer the question,
        say "Unknown".ImportError

        """,
    )
    chain = LLMChain(llm=llm, prompt = prompt)
    response = chain.run(question=query)
    response = response.replace("\n", "")
    return response