from mcp_agent.mock_test_agent import *
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
import os
from dotenv import load_dotenv
from mcp_agent.mcp_client import delete_mcp_client
import re
import requests
from PIL import Image
import io

load_dotenv(dotenv_path="mcp_agent/.env")
    
def display_check_tool_call(state):
    last_message = state.values["messages"][-1]
    return last_message.tool_calls[0]

def get_last_tool_message_and_last_ai_message(response):
    last_message = response["messages"][-1]
    last_tool_message = None
    if isinstance(response["messages"][-2], ToolMessage):
        print("Chui vao Tool Message")
        last_tool_message = response["messages"][-2]
        print(last_tool_message)
    return last_message, last_tool_message

# def get_last_tool_message_and_last_ai_message(response):
#     messages = response["messages"]
    
#     last_ai_message = None
#     last_tool_message = None

#     # Duyệt ngược để tìm AIMessage cuối cùng và ToolMessage gần đó
#     for msg in reversed(messages):
#         if last_ai_message is None and isinstance(msg, AIMessage):
#             last_ai_message = msg
#         if last_tool_message is None and isinstance(msg, ToolMessage):
#             last_tool_message = msg
#         if last_ai_message and last_tool_message:
#             break

#     return last_ai_message, last_tool_message

def get_url_from_str(input_string):
    print("Da vao get url")
    print(input_string)
    match = re.search(r"text='(https?://[^']+)'", input_string)

    if match:
        url = match.group(1)
        print("URL ma ta lay duoc: ", url)
        return url
    
    return None

def get_image_from_url(image_url):
    print("Da vao ham get image")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.0.0 Safari/537.36"
    }
    response = requests.get(image_url, headers=headers)
    print("Thuc hien xong get")
    image = Image.open(io.BytesIO(response.content))
    print("Thuc hien xong chuyen doi")
    return image

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
    await delete_mcp_client()
    
    if isinstance(last_message_in_state, AIMessage) and last_message_in_state.tool_calls:
        return state, "confirm"
    
    last_message, last_tool_message = get_last_tool_message_and_last_ai_message(response)
    url = get_url_from_str(last_tool_message.content)
    image = get_image_from_url(url)
    bot_response = last_message.content
    print("URL: ", url)
    
    return bot_response, image, response, "END"




    