from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import Bedrock
from langchain.memory import ConversationBufferMemory
import boto3
import os
import streamlit as st

os.environ["AWS_PROFILE"] = "zmattes"

#bedrock client

bedrock_client = boto3.client(
    service_name = "bedrock-runtime",
    region_name = "us-east-1"
)

modelID = "anthropic.claude-v2:1"

llm = Bedrock(
    model_id=modelID,
    client=bedrock_client,
    model_kwargs={"max_tokens_to_sample": 200, "temperature": 0.9}

)

def my_chatbot(language, freeform_text):
    prompt = PromptTemplate(
        input_variables=["language", "freeform_text"],
        template="You are a chatbot. You are in {language}.\n\n{freeform_text}"

    )

    bedrock_chain = LLMChain(llm=llm, prompt=prompt)
    response=bedrock_chain.invoke({'language': language, 'freeform_text': freeform_text})
    return response

#print(my_chatbot("English", "which country has the largest economy"))

st.title("Board Game Bob")

language = st.sidebar.selectbox("Language", ["english", "spanish"])

if language:
    freeform_text = st.sidebar.text_area(label="what is your question?", max_chars=100)
if freeform_text:
    response = my_chatbot(language, freeform_text)
    st.write(response['text'])