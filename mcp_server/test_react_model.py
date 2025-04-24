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


load_dotenv()
model_name = os.getenv("MODEL_NAME")
print("Model: ", model_name)

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

def parse_json_from_draw_bar_chart_response(json_string):
    image_bytes = ast.literal_eval(json_string)
    image = Image.open(io.BytesIO(image_bytes))
    image.show()
    return image

def parse_json_from_get_column_from_dataset_response(json_string):
    dict_list = json.loads(json_string)

    return dict_list

parse_type_mapping = {
    "get_all_orders": parse_json_from_get_all_orders_response,
    "draw_bar_chart": parse_json_from_draw_bar_chart_response,
    "get_column_from_dataset": parse_json_from_get_column_from_dataset_response
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
        agent = create_react_agent(model, client.get_tools())
        message = "draw chart to compare the frequency of each order status value in the order_dataset table"
        # print(client.get_tools()[0].args_schema)
        response = await agent.ainvoke({"messages": message})


        # tool_messages = [msg for msg in response['messages'] if isinstance(msg, ToolMessage)]
        
        
        # for ms in response["messages"]:
        #     ms.pretty_print()

        # print("Response: ", response['messages'][-1])
        # tools = client.get_tools()
        # print(tools[3].args_schema)




if __name__ == "__main__":
    asyncio.run(main())