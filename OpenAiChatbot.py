import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


import os 
from dotenv import load_dotenv

load_dotenv()

#langsmith tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"]="Q&A Chatbot With OpenAI"


## Prompt Template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant.Please response to the user question"),
        ("user", "Question:{question}"),
    ]
)

def generate_response(question,api_key,engine,temperature,max_tokens):
    openai.api_key = api_key
    llm=ChatOpenAI(model=engine,api_key=api_key)
    output_parser=StrOutputParser()
    chain=prompt | llm | output_parser
    answer=chain.invoke({"question":question})
    return answer


## Streamlit 
## Titel of the app
st.title("Q&A Chatbot with OpenAI")

## Sidebar for settings
st.sidebar.title("Settings")
api_key=st.sidebar.text_input("Enter your OpenAI API Key:",type="password")

## Drop down to select various Open AI models
llm=st.sidebar.selectbox("Select an Open AI model",["gpt-4o","gpt-4-turbo","gpt-4"])

temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.5)
max_tokens=st.sidebar.slider("Max Tokens",min_value=50,max_value=300,value=150)


## Main interface for user input
st.write("Go ahead and ask any question!")
user_input=st.text_input("You:")

if user_input and api_key:
    response=generate_response(user_input,api_key,llm,temperature,max_tokens)
    st.write(response)
elif user_input:
    st.warning("Please enter the OpenAI API key in the sidebar.")
else:
    st.write("Please enter a question to get a response.")