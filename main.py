from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import Bedrock
from langchain.memory import ConversationBufferMemory
import boto3
import os
import streamlit as st
import pandas as pd
import sqlite3

df_boardgames_csv = pd.read_csv("./boardgames_ranks.csv")
df_boardgames_csv.set_index("id", inplace=True)

connection = sqlite3.connect(":memory:")
df_boardgames_csv.to_sql("boardgames", connection, index=False, if_exists="replace")
schema = str(df_boardgames_csv.dtypes)



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
        template="You are a chatbot. You are in {language}. I want you to answer the question in a SQL statement using the 'boardgames' table.\n"
                "The table schema is as follows:\n"
                "{schema}\n"
                "Do not include any explanation and just provide the SQL statement."
                "For ranks the the lower numbers means its a better game than others that have a bigger number."
                "If the value of the rank is None or 0 that means it is not good and should NOT be suggested when asking for best."
                "If the question doesn't involve boardgames, say you can't answer it.\n\n"
                "{freeform_text}"

    )

    bedrock_chain = LLMChain(llm=llm, prompt=prompt)
    generated_sql = bedrock_chain.run({"language": language, "freeform_text": freeform_text, "schema": schema})

    try: 
        result = pd.read_sql_query(generated_sql, connection)
        return result
    except Exception as e:
        return f"error: {str(e)}" 





#print(my_chatbot("English", "which country has the largest economy"))
#print(my_chatbot("English", "What is the number one strategic board game?"))

st.title("Board Game Bob")

language = st.sidebar.selectbox("Language", ["english", "spanish"])

if language:
    freeform_text = st.sidebar.text_area(label="what is your question?", max_chars=100)
if freeform_text:
    response = my_chatbot(language, freeform_text)
    st.write(response)

