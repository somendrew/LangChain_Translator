""" 
It consists of three things:

1. The definition of our chain that we just built above
2. Our FastAPI app
3. A definition of a route from which to serve the chain, which is done with langserve.add_routes

"""
from sam_sk import api_key
from fastapi import FastAPI 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langserve import add_routes


#1. Create prompt template

system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ("system" , system_template),
    ("user" ,"{text}"),
])

#2. create model
model = ChatGroq(api_key=api_key)

#3. Create Parser
parser = StrOutputParser()

#4. crate chain
chain = prompt_template | model | parser

#5. App definition
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API using langchain runnable interfaces",
)

#6. Adding Chain route
add_routes(
    app,
    chain,
    path="/chain",
)

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app,host="localhost",port= 8002)