# import modules.logger_tool as logger

import os
from fastapi import APIRouter, Depends
from dependencies import admin_dependency

from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate

router = APIRouter()

# logging = logger.get_logger(os.environ['LOG_NAME'], log_level=os.environ['LOG_LEVEL'], log_path=os.environ['LOG_DIR'], log_file=os.environ['LOG_NAME'])

@router.get("/prompt")
async def query_graph(prompt: str):
    graph = Neo4jGraph(
    url=f"bolt://{os.environ['NEO4J_HOST']}:{os.environ['NEO4J_BOLT_PORT']}", username=os.environ['NEO4J_USER'], password=os.environ['NEO4J_PASSWORD']
    )

    graph.refresh_schema()

    CYPHER_GENERATION_TEMPLATE = """Task:Generate Cypher statement to query a graph database.
    Role:
    You are an assistant in a school for staff, and you specialize in querying graph databases to find answers to questions.

    Instructions:
    Use only the provided relationship types and properties in the schema.
    Do not use any other relationship types or properties that are not provided.

    Schema:
    {schema}

    Note: Do not include any explanations or apologies in your responses.
    Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
    Do not include any text except the generated Cypher statement.

    The question is:
    {question}"""

    CYPHER_GENERATION_PROMPT = PromptTemplate(
        input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
    )

    chain = GraphCypherQAChain.from_llm(
        graph=graph,
        cypher_llm=ChatOpenAI(temperature=0, model="gpt-4-1106-preview"),
        qa_llm=ChatOpenAI(temperature=0, model="gpt-4-1106-preview"),
        top_k=20,
        verbose=True,
        cypher_prompt=CYPHER_GENERATION_PROMPT,
        return_intermediate_steps=True,
        exclude_types=[],
        include_types=[]
    )
    
    return chain(prompt)