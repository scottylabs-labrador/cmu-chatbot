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
        You are a filtering assistant, who extracts information from user input.
        Based on the following question: "{question}", extract the numeric data only for course units/credits, course level range, and FCE ratings.

        Return in the form of a JSON with the keys "units", "course level", and "FCE". If there is no information for that key in the user input, make the data value for the entry "void".  Course level includes "undergraduate" or "graduate". Only return the bare JSON file and nothing else.

        If you feel like you don't have enough information to answer the question.set,
        say "Unknown".ImportError

        """,
    )
    chain = LLMChain(llm=llm, prompt = prompt)
    response = chain.run(question=query)
    response = response.replace("\n", "")
    return response