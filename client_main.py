from mcp_agent.mock_test_agent import *
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
import os
from dotenv import load_dotenv
from mcp_agent.mcp_client import delete_mcp_client
import re
import requests
from PIL import Image
import io
import json
import pandas as pd

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
    return last_message, last_tool_message

def get_json_string_sql_result(input_json_string):
    match = re.search(r'\[.*\]', input_json_string)

    if match:
        json_array_str = match.group(0)
        return json_array_str
    
    return None

def convert_list_of_dict(list_of_dict):
    result = {}

    for item in list_of_dict:
        for key, value in item.items():
            result.setdefault(key, []).append(value)

    return result

def extract_filepath(text):
    print("Extracting file path from text")
    match = re.search(r'path\s+([A-Z]:\\[^\s,]+)', text)
    if match:
        return match.group(1)
    return None

def handle_json_result(returned_content):
    json_string = get_json_string_sql_result(returned_content)
    result = None
    if json_string:
        result = json.loads(json_string)
        result = convert_list_of_dict(result)
    else:
        file_path = extract_filepath(returned_content)
        df = pd.read_csv(file_path)
        result = df.to_dict(orient='list')

    return result

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

def handle_image_result(returned_content):
    url = get_url_from_str(returned_content)
    image = get_image_from_url(url)
    return image

def handle_user_accept_tool(input_from_user, state):
    state.values["user_confirmation"] = input_from_user
    if input_from_user == "no":
        reply_aimessages = AIMessage(content="I will not use this tool")

        for key, value in reply_aimessages.__dict__.items():
            if key != 'id':
                setattr(state.values["messages"][-1], key, value)
    return state

handle_result_for_each_tool = {
    "draw_bar_chart": handle_image_result,
    "draw_barh_chart": handle_image_result,
    "draw_boxplot_chart": handle_image_result,
    "draw_hist_chart": handle_image_result,
    "draw_line_chart": handle_image_result,
    "draw_pie_chart": handle_image_result,
    "draw_scatter_chart": handle_image_result,
    "draw_pearson_correlation_chart": handle_image_result,
    "sql_tool": handle_json_result
}

# --- Example Usage ---
async def ask_agent(agent, input_prompt: str , thread, new_state = None):
    if input_prompt:
        messages = [HumanMessage(content=input_prompt)]
    else:
        messages = None
    print(f"Input prompt: {input_prompt}")

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
    bot_response = last_message.content

    print(last_tool_message)


    tool_result = None

    if last_tool_message:
        tool_name = last_tool_message.name
        tool_content = last_tool_message.content
        
        if tool_name in handle_result_for_each_tool:
            handle_func = handle_result_for_each_tool[tool_name]
            tool_result = handle_func(tool_content)

    
    return bot_response, tool_result, response, "END"




    