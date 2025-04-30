from mcp_agent.agent_gemini import DataAgentGraph
from mcp_agent.mock_test_agent import *
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
import os
from dotenv import load_dotenv
from mcp_agent.mcp_client import get_mcp_client, delete_mcp_client
import re
import requests
from PIL import Image
import io

load_dotenv(dotenv_path="mcp_agent/.env")
    
def display_check_tool_call(state):
    last_message = state.values["messages"][-1]
    return last_message.tool_calls[0]

def get_last_tool_message_and_last_ai_message(reponse):
    last_message = reponse["messages"][-1].content
    last_tool_message = None
    if isinstance(last_tool_message, ToolMessage):
        print("Chui vao Tool Message")
        last_tool_message = reponse["messages"][-2]
    return last_message, last_tool_message

def get_url_from_str(input_string):
    match = re.search(r"text='(https?://[^']+)'", input_string)

    if match:
        url = match.group(1)
        return url
    
    return None

def get_image_from_url(image_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.0.0 Safari/537.36"
    }
    response = requests.get(image_url, headers=headers)
    image = Image.open(io.BytesIO(response.content))
    image.show()

def handle_user_accept_tool(input_from_user, state):
    state.values["user_confirmation"] = input_from_user
    if input_from_user == "no":
        state.values["messages"].pop()
        reply_aimessages = AIMessage(content="I will not use this tool")
        state.values["messages"].append(reply_aimessages)
    return state

# --- Example Usage ---
async def ask_agent(agent, input_prompt: str , thread, new_state = None):
    if input_prompt:
        messages = [HumanMessage(content=input_prompt)]
    else:
        messages = None

    if new_state:
        await agent.graph.aupdate_state(thread, new_state.values)
        response = await agent.graph.ainvoke(None, thread)
    else:
        response = await agent.graph.ainvoke({"messages": messages}, thread)

    state = await agent.graph.aget_state(thread)
    
    last_message_in_state = state.values["messages"][-1]
    print("===================================================================================")

    for msg in state.values["messages"]:
        msg.pretty_print()
    
    if isinstance(last_message_in_state, AIMessage) and last_message_in_state.tool_calls:
        return state, "confirm"
    
    return response, "END"

async def test():
    messages = "Draw a grouped bar chart to compare number of goals and assistes of messi and ronaldo, where messi scored 98 goals and ronaldo scored 100 goals and messi assisted 100 and ronaldo assisted 98"
    MODEL_NAME  = os.getenv("MODEL_NAME")
    llm = ChatGoogleGenerativeAI(model=MODEL_NAME, temperature = 0.0)
    agent = DataAgentGraph(llm=llm, server_url="http://localhost:8000/sse")
    thread = {"configurable": {"thread_id": "1"}}
    state, next_action = await ask_agent(agent, messages, thread)
    tool_call_json = display_check_tool_call(state)
    print(tool_call_json)

    input_from_user = input("yes/no")

    state = handle_user_accept_tool(input_from_user, state)

    # Tham khao de kiem tra print(state.values["messages"][-1].tool_calls)
    response, next_action = await ask_agent(agent, messages, thread, state)
    print(next_action)
    last_message, last_tool_message = get_last_tool_message_and_last_ai_message(response)
    print(last_message)
    print(last_tool_message)
    if last_tool_message:
        print(last_tool_message.name)
        url = get_url_from_str(last_tool_message.content)
        get_image_from_url(url)
    else:
        print("Thang lay khong goi tool")
    await delete_mcp_client()

if __name__ == "__main__":
    import asyncio

    try:
        asyncio.run(test())
    except KeyboardInterrupt:
        print("End")

    # # # Replace with your actual LLM instance
    # # try:
    # #     # Use OpenAI or another supported LLM
    # #     model_type = os.getenv("MODEL_TYPE")
    # #     model_name = os.getenv("MODEL_NAME")
    # #     print(model_name)
        
    # #     if model_type == "OPEN_AI":
    # #         from langchain_openai import ChatOpenAI
    # #         # from langchain_google_genai import ChatGoogleGenerativeAI
    # #         # Ensure API keys are set (e.g., OPENAI_API_KEY environment variable)
    # #         llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, streaming=True)
    # #         # llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0, streaming=True)
    # #     elif model_type == "GEMINI":
    # #         llm = ChatGoogleGenerativeAI(model = model_name, temperature=0.0)
    # #     else:
    # #         raise NameError(f"Not support model {model_type}")
    # # except ImportError:
    # #     print("Error: Langchain OpenAI/Google not installed. Add 'langchain-openai' or 'langchain-google-genai' to your requirements.")
    # #     return
    # # except Exception as e:
    # #     print(f"Error initializing LLM: {e}")
    # #     print("Ensure your API key is set correctly.")
    # #     return
    # if input_prompt:
    #     message = HumanMessage(input_prompt)
    # else:
    #     message = input_prompt

    # response = await agent.graph.ainvoke({"messages": [message]}, thread)

    # state = await agent.graph.aget_state(thread)

    # # if state.next:
    # #     return state, state.next[0]
    
    # # tool_msg = [msg for msg in response["messages"] if isinstance(msg, ToolMessage)]

    # _id = state.values["messages"][-1].tool_calls[0]['id']
    # state.values['messages'][-1].tool_calls =[
    #     {
    #         'name': 'draw_bar_chart',
    #         'args': {
    #             'y_label': 'Count',
    #             'title': 'Goal and Assists',
    #             'type': 'grouped',
    #             'y_data': {'Goals': [98.0, 100.0], 'Assists': [100.0, 100.0]},
    #             'x_label': 'Player',
    #             'x_data': ['Messi', 'Ronaldo']
    #         },
    #         'id': _id
    #     }
    # ]
    # new_agent = DataAgentGraph(llm=llm, server_url=mcp_server_url)
    # await new_agent.graph.aupdate_state(thread, state.values)
    # state = await new_agent.graph.aget_state(thread)
    # print(state.values["messages"][-1].tool_calls)
    # # response = await new_agent.graph.ainvoke(None, thread)
    # # print(response['messages'][-2])
    # response = await new_agent.graph.ainvoke(None, thread)

    # await delete_mcp_client()
                
    # return response





    