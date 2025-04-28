from mcp_agent.agent_gemini import DataAgentGraph
from mcp_agent.mock_test_agent import *
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="mcp_agent/.env")
# --- Example Usage ---
async def main():
    # Replace with your actual LLM instance
    try:
        # Use OpenAI or another supported LLM
        model_type = os.getenv("MODEL_TYPE")
        model_name = os.getenv("MODEL_NAME")
        print(model_name)
        
        if model_type == "OPEN_AI":
            from langchain_openai import ChatOpenAI
            # from langchain_google_genai import ChatGoogleGenerativeAI
            # Ensure API keys are set (e.g., OPENAI_API_KEY environment variable)
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, streaming=True)
            # llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0, streaming=True)
        elif model_type == "GEMINI":
            llm = ChatGoogleGenerativeAI(model = model_name, temperature=0.0)
        else:
            raise NameError(f"Not support model {model_type}")
    except ImportError:
        print("Error: Langchain OpenAI/Google not installed. Add 'langchain-openai' or 'langchain-google-genai' to your requirements.")
        return
    except Exception as e:
        print(f"Error initializing LLM: {e}")
        print("Ensure your API key is set correctly.")
        return

    # Replace with the actual URL of your MCP server
    mcp_server_url = "http://localhost:8000/sse" # Example URL

    agent = DataAgentGraph(llm=llm, server_url=mcp_server_url)
    

    # --- Interactive Chat Loop ---
    current_thread_id = None
    while True:
        if current_thread_id:
             prompt = input(f"\n[Thread: {current_thread_id}] Your next message (or type 'exit' or 'new'): \n> ")
        else:
             prompt = input("\nHello! What data analysis task can I help you with today? (or type 'exit')\n> ")

        if prompt.lower() == 'exit':
            break
        if prompt.lower() == 'new':
            current_thread_id = None
            print("Starting a new conversation thread.")
            continue # Go to the start of the loop for the initial prompt

        if prompt:
            try:
                # Pass the current_thread_id to continue the conversation
                current_thread_id = await agent.run_conversation(prompt, thread_id=current_thread_id)
            except Exception as e:
                 print(f"\nAn error occurred during the conversation: {e}")
                 # Optionally reset thread or try to recover
                 # current_thread_id = None # Reset to start new on error?
        else:
             print("Empty input, please provide a query.")

if __name__ == "__main__":
    import asyncio
    import platform

    # Fix for known issue with asyncio on Windows + Python 3.8+
    # if platform.system() == "Windows":
    #     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting...")