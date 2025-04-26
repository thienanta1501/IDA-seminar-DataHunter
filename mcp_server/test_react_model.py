import asyncio
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import ast
from PIL import Image
import io
from langchain_core.messages.tool import ToolMessage
import json
import requests


load_dotenv()
model_name = os.getenv("MODEL_NAME")
print("Model: ", model_name)

def get_image_from_url(image_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.0.0 Safari/537.36"
    }
    response = requests.get(image_url, headers=headers)
    image = Image.open(io.BytesIO(response.content))
    image.show()


def print_stream(stream):
    for s in stream:
        message = s['messages'][-1]

        if isinstance(message, tuple):
            print(message)
            print("Message is tuple")
        else:
            # message.pretty_print()
            # print("Message is not tuple")
            print(message)

def parse_json_from_get_all_orders_response(json_string):
    dict_list = json.loads(json_string)

    result = [json.loads(item) for item in dict_list]
    return result

def parse_json_from_image_response(json_string):
    image_bytes = ast.literal_eval(json_string)
    image = Image.open(io.BytesIO(image_bytes))
    image.show()
    return image

def parse_json_from_image(json_string):
    image_bytes = ast.literal_eval(json_string)
    image = Image.open(io.BytesIO(image_bytes))
    image.show()
    return image

def parse_json_from_get_column_from_dataset_response(json_string):
    dict_list = json.loads(json_string)

    return dict_list

parse_type_mapping = {
    "get_all_orders": parse_json_from_get_all_orders_response,
    "get_column_from_dataset": parse_json_from_get_column_from_dataset_response,
    "draw_bar_chart": get_image_from_url,
    "draw_boxplot_chart": get_image_from_url,
    "draw_distribution_chart": get_image_from_url,
    "draw_line_chart": get_image_from_url,
    "draw_pie_chart": get_image_from_url,
    "draw_scatter_chart": get_image_from_url,
    "draw_stackplot_chart": get_image_from_url,
    "draw_violinplot_chart": get_image_from_url
    
}

async def main():
    model = ChatGoogleGenerativeAI(
        model=model_name,
        temperature=0.0
    )

    async with MultiServerMCPClient(
        {
            "Thanh server": {
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            }
        }
    ) as client:
        agent = create_react_agent(model, tools=client.get_tools())

        message = "Draw a grouped bar chart to compare number of goals and assistes of messi and ronaldo, where messi scored 98 goals and ronaldo scored 100 goals \
            and messi assisted 100 and ronaldo assisted 98"
        # print(client.get_tools()[0].args_schema)
        response = await agent.ainvoke({"messages": message})
        for msg in response["messages"]:
            msg.pretty_print()

        tool_messages = [msg for msg in response['messages'] if isinstance(msg, ToolMessage)]

        for msg in tool_messages:
            tool_name = msg.name
    
            content = msg.content
            if tool_name in parse_type_mapping:
                parse_function = parse_type_mapping[tool_name]
                parse_data = parse_function(content)


if __name__ == "__main__":
    asyncio.run(main())