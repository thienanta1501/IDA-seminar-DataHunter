from mcp_agent.agent_gemini import DataAgentGraph
from mcp_agent.mock_test_agent import *
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
import os
from dotenv import load_dotenv
from mcp_agent.mcp_client import get_mcp_client, delete_mcp_client

load_dotenv(dotenv_path="mcp_agent/.env")
    


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

    # await delete_mcp_client()
    
    last_message_in_state = state.values["messages"][-1]
    print(last_message_in_state)
    
    # if hasattr(last_message_in_state, "additional_kwargs"):
    #     if "function_call" in last_message_in_state.additional_kwargs:
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

    state.values["user_confirmation"] = "no" # yes/no

    if state.values["user_confirmation"] == "no":
        state.values["messages"].pop()
        reply_aimessages = AIMessage(content="I will not use this tool")
        state.values["messages"].append(reply_aimessages)
    # Tham khao de kiem tra print(state.values["messages"][-1].tool_calls)
    response, next_action = await ask_agent(agent, messages, thread, state)
    print(next_action)
    await delete_mcp_client()

# if __name__ == "__main__":
#     import asyncio

#     try:
#         asyncio.run(test())
#     except KeyboardInterrupt:
#         print("End")

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





    