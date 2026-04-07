import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
print(llm.invoke("What is the capital of France?").content)