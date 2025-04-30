from mcp_agent.agent_gemini import DataAgentGraph
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv("mcp_agent\.env")

model_name = os.getenv("MODEL_NAME")
llm = ChatGoogleGenerativeAI(
    model=model_name,
    temperature=0.0
)
server_url="http://localhost:8000/sse"
agent = DataAgentGraph(llm=llm, server_url=server_url)
thread = {"configurable": {"thread_id": "1"}}