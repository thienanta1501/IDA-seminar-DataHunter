# Required imports
import json
# import sqlite3 # Removed
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, TypedDict, Annotated, Sequence, Union
import operator
from typing_extensions import TypedDict

from langchain_core.language_models import BaseLanguageModel
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage, SystemMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import BaseTool, ToolException
from pydantic import BaseModel, Field

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.types import interrupt
# from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver # Removed
from langgraph.checkpoint.memory import MemorySaver # Added MemorySaver


# Assuming these are correctly defined elsewhere or mocked as before
#from mcp_agent.tools.db_tools import DBStructureTool, SQLTool
#from mcp_agent.tools.ml_tools import MLModelTool
#from mcp_agent.tools.visualization_tools import VisualizationTool
from mcp_agent.mcp_client import MCPClient
from mcp_agent.tools.db_tools import get_db_structure, sql_tool
from mcp_agent.tools.visualization_tools import draw_barh_chart, draw_boxplot_chart, \
draw_hist_chart, draw_line_chart, draw_pie_chart, draw_scatter_chart, draw_pearson_correlation_chart, draw_bar_chart
from mcp_agent.tools.stats_tool import generate_html_report
from mcp_agent.mock_test_agent import mock_build_ml_model, mock_get_db_structure, mock_sql_tool, mock_visualize_tool
from uuid import uuid4
# --- Removed Database Setup for Chat History ---
# DB_FILE = "data_agent_history.db" # Removed
# init_db() and log_message_to_db() functions are removed
def reduce_messages(left: Sequence[BaseMessage], right: Sequence[BaseMessage]) -> Sequence[BaseMessage]:
    # assign ids to messages that don't have them
    for message in right:
        if not message.id:
            message.id = str(uuid4())
    # merge the new messages with the existing messages
    merged = left.copy()
    for message in right:
        for i, existing in enumerate(merged):
            # replace any existing messages with the same id
            if existing.id == message.id:
                merged[i] = message
                break
        else:
            # append any new messages to the end
            merged.append(message)
    return merged

class AgentState(TypedDict):
    # Explicitly tell LangGraph to append messages using operator.add
    messages: Annotated[Sequence[BaseMessage], reduce_messages]
    thread_id: Annotated[str, "The unique ID for the conversation thread"]
    db_schema: Annotated[Optional[str], "The database schema description"]
    data_retrieved: Annotated[bool, "Flag indicating if data has been successfully retrieved via SQLTool"]
    proposed_tool_call: Annotated[Optional[Dict], "The tool call the agent proposes to execute"]
    user_confirmation: Annotated[str, "User response ('yes'/'no') to the proposed tool call"]
    
# --- DataAgentGraph Class ---
class DataAgentGraph:
    """
    LangGraph-based agent for AI-Driven Data Analysis with Human-in-the-Loop,
    workflow constraints, and persistence using MemorySaver. Interacts with an MCP Server.
    """

    def __init__(self, llm: BaseLanguageModel, server_url: str):
        """Initialize the DataAgentGraph.

        Args:
            llm: The language model to use.
            server_url: URL of the MCP server for tool execution.
        """
        self.llm = llm
        self.server_url = server_url

        # Create tools
        self.tools = self._create_tools()
        self.llm_with_tools = self.llm.bind_tools(self.tools)

        self.memory = MemorySaver() # Use MemorySaver

        # Create the graph
        self.graph = self._create_graph()

        # Initialize MCPClient (optional)
        # try:
        #     self.mcp_client = MCPClient()
        #     # self.mcp_client.connect_to_sse_server(self.server_url)
        # except NameError:
        #     print("MCPClient not available/mocked, skipping connection.")
        #     self.mcp_client = None

        #print(self.tools)
    def _create_tools(self) -> list:
        """Create the tools for the agent."""
        # Removed duplicate mock_visualize_tool
        return [
            get_db_structure,
            sql_tool,
            mock_visualize_tool,
            mock_build_ml_model,
            draw_barh_chart,
            draw_boxplot_chart,
            draw_hist_chart,
            draw_line_chart,
            draw_pie_chart,
            draw_scatter_chart,
            draw_pearson_correlation_chart,
            draw_bar_chart,
            generate_html_report
        ]

    # --- Graph Nodes ---

    async def check_initial_state(self, state: AgentState) -> Dict[str, Any]: # Return type changed to Dict for clarity
        """
        Node to fetch DB schema if not already present.
        Returns only the state updates needed.
        """
        print("--- CHECKING INITIAL STATE ---")
        # Check if 'db_schema' key exists and is not None in the loaded state
        if state.get("db_schema") is None:
            print("DB Schema not found in state, attempting to fetch...")
            # We don't need the current messages list here, as we return only updates

            db_structure_tool = self.tools[0]
            #print(db_structure_tool)
            tool_call_id = str(uuid.uuid4())
            ai_message = AIMessage(
                content="First, I need to retrieve the database structure.",
                tool_calls=[{
                    "id": tool_call_id,
                    "name": "get_db_structure",
                    "args": {}
                }]
            )

            try:
                try:
                    response = await db_structure_tool()
                except Exception as e:
                    print("*"*20)
                    print(e)

                db_schema = str(response)
                tool_message = ToolMessage(
                    content=db_schema,
                    tool_call_id=tool_call_id,
                    name="get_db_structure"
                )

                ###print(f"DB Schema retrieved:\n{db_schema[:500]}...")
                # Return ONLY the updates: the new schema and the messages added in this step
                return {
                    "db_schema": db_schema,
                    "messages": [ai_message, tool_message],
                }
            except Exception as e:
                print(f"Error fetching DB Schema: {e}")
                error_message = AIMessage(content=f"Error fetching database structure: {str(e)}")
                # Return only the error message to be appended
                # Also return potentially the AI message that tried to call the tool if needed?
                # Let's just return the error message for now.
                return {
                    "messages": [ai_message, ToolMessage(content=f"Error calling tool: {e}", tool_call_id=tool_call_id)] # Or just the error AI message
                    # Alternative: return {"messages": [error_message]}
                }
        else:
            print("DB Schema already present in state.")
            # No updates needed, return empty dict
            return {}

    
    def plan_action(self, state: AgentState) -> Dict[str, Any]: # Return type Dict
        """
        Node to decide the next action based on the conversation history,
        available data, DB schema, and workflow constraints.
        Invokes the LLM with tools. Returns only updates.
        """
        ###print("--- PLANNING ACTION ---")
        # --- Add this Debug Print ---
        ###print(f"DEBUG plan_action: Received state['messages'] length: {len(state['messages'])}")
        if state['messages']:
             print(f"DEBUG plan_action: Last message type: {type(state['messages'][-1])}, content snippet: {str(state['messages'][-1].content)[:50]}...")
        # --- End Debug Print ---

        print("--- PLANNING ACTION ---")
        system_prompt = f"""You are a highly skilled Data Analyst assistant. Your goal is to help users analyze data using a database.
                            You can perform the following actions by calling the appropriate tools:
                            1.  **Retrieve Database Structure**: Understand the tables and columns available (using `get_db_structure` - usually done automatically first).
                            2.  **Generate & Execute SQL**: Write and run SQL queries based on user requests in natural language (using `sql_tool`).
                            3.  **Visualize Data**: Create visualizations (plots, charts) from retrieved data (using `visualize_tool`). Requires data to be retrieved first (data_retrieved=True).
                            4.  **Build ML Models**: Train basic ML models like Naive Bayes, Decision Tree, Clustering, Linear Regression (using `build_ml_model`). Requires data to be retrieved first (data_retrieved=True).

                            **Database Schema:**
                            {state.get('db_schema', 'Not available yet. Fetching or provide if error.')}

                            **Current Data Status:** Data has {'already' if state.get('data_retrieved') else 'NOT'} been retrieved via an SQL query in this session.

                            **Workflow Rules & Constraints:**
                            * You **MUST** have the database structure before proceeding (usually handled automatically). If there was an error getting it, inform the user.
                            * You **MUST** execute an SQL query using `sql_tool` and confirm data has been retrieved (`data_retrieved` state is True) **BEFORE** you can use `visualize_tool` or `build_ml_model`.
                            * If the user asks for visualization or ML *without* prior data retrieval, you **MUST** first plan and execute an `sql_tool` call to get the necessary data. Ask clarifying questions if the required data isn't obvious.
                            * Break down complex requests into logical steps.
                            * When you decide to use a tool, the user will be asked for confirmation before it runs. Explain clearly why you are choosing a specific tool and what arguments you plan to use.

                            Based on the latest user message and the conversation history (including tool results), decide the next single action. This could be:
                            - Calling ONE tool (e.g., `sql_tool`, `visualize_tool`, `build_ml_model`).
                            - Asking the user a clarifying question.
                            - Providing a final answer if the task is complete.
                            """

        # Construct prompt messages using the messages from the *current* state
        prompt_messages = [SystemMessage(content=system_prompt)] + state["messages"]
        len_prompt = len(prompt_messages)
        print("Trong plan")
        if len_prompt > 5:
            attributes = dir(prompt_messages[4])
            print(type(attributes))

        print("Invoking LLM with messages:")
        # (Optional) Print condensed message history for debugging
        ###for i, msg in enumerate(prompt_messages):
        ###    print(f"[{i}] {msg.type}: {str(msg.content)[:200]}...")

        ai_response = self.llm_with_tools.invoke(prompt_messages)

        ### print(f"DEBUG plan_action: LLM response content: '{ai_response.content}'")
        ### print(f"DEBUG plan_action: LLM response tool_calls: {getattr(ai_response, 'tool_calls', None)}")

        # --- End Debug Print ---
        # Return the updates
        return {
            "messages": [ai_response], 
            "user_confirmation": "no"
        }

    def human_in_the_loop_confirmation(self, state: AgentState) -> AgentState:
        """Node to ask the user for confirmation before executing a proposed tool."""
        print("--- HUMAN IN THE LOOP ---")
        ai_message = state["messages"][-1]

        if not isinstance(ai_message, AIMessage) or not ai_message.tool_calls:
            print("No tool call proposed by AI in the last message.")
            return {**state, "proposed_tool_call": None, "user_confirmation": "error_no_tool_call"}

        tool_call = ai_message.tool_calls[0]
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_call_id = tool_call["id"]

        proposed_tool_call_details = {"id": tool_call_id, "name": tool_name, "args": tool_args}
        current_messages = list(state["messages"]) # No need to copy, state is immutable per step

        # Workflow Constraint Check
        if tool_name in ["mock_visualize_tool", "mock_build_ml_model"] and not state.get("data_retrieved"):
            print(f"Workflow Constraint Violation: Cannot use {tool_name} before data is retrieved.")
            constraint_message = AIMessage(
                content=f"Hold on! To use the `{tool_name}`, we first need to retrieve some data using the `sql_tool`. "
                        f"The database schema is:\n```\n{state.get('db_schema', 'Not available')}\n```\n"
                        f"Could you please specify what data you'd like to fetch for this task, or confirm if I should try to infer it?"
            )
            # Return state update: add constraint message, block proposal
            return {
                "messages": [constraint_message], # LangGraph appends this
                "proposed_tool_call": None,
                "user_confirmation": "constraint_violation"
            }

        print(f"\nProposed action: Use tool '{tool_name}' with arguments:")
        print(json.dumps(tool_args, indent=2))
        print(f"(Internal Tool Call ID: {tool_call_id})")

        # feedback = interrupt("Do you want to proceed with this action? (yes/no): ")

        # while True:
        #     confirmation = input("Do you want to proceed with this action? (yes/no): ").strip().lower()
        #     if confirmation in ["yes", "no"]:
        #         break
        #     else:
        #         print("Invalid input. Please enter 'yes' or 'no'.")

        # if confirmation == "no":
        #     print("User rejected the action.")
        #     state["messages"].pop()
        #     rejection_message = HumanMessage(content="No, I don't want to proceed with that action.")
        #     clarification_request = AIMessage(content="Okay, I won't proceed with that tool call. How would you like to modify the request, or what should I do instead?")
        #     # Return state update: add rejection/clarification messages, clear proposal
        #     return {
        #          "messages": [rejection_message, clarification_request], # Append these
        #          "proposed_tool_call": None,
        #          "user_confirmation": "no"
        #      }
        # else: # confirmation == "yes"
        #     print("User confirmed the action.")
        #     # Return state update: store confirmed call, set confirmation flag
        #     # No new messages needed here, just state flags.
        return {
                "proposed_tool_call": proposed_tool_call_details, # Update this field
                "user_confirmation": "yes"
                # No message update needed here
            }

    def check_sql_success(self, state: AgentState) -> AgentState:
        """Node to update data_retrieved flag after sql_tool execution."""
        print("--- CHECKING SQL SUCCESS ---")
        last_message = state["messages"][-1]
        data_retrieved = state.get("data_retrieved", False) # Get current value

        if isinstance(last_message, ToolMessage):
            tool_call_id = last_message.tool_call_id
            original_tool_name = None

            # Find the corresponding AI message that made the call
            for msg in reversed(state["messages"][:-1]):
                if isinstance(msg, AIMessage) and msg.tool_calls:
                    for tc in msg.tool_calls:
                        if tc['id'] == tool_call_id:
                            original_tool_name = tc['name']
                            break
                if original_tool_name:
                    break

            if original_tool_name == "mock_sql_tool":
                # Basic success check (adjust if your mock tool returns specific error formats)
                if "error" not in str(last_message.content).lower() and last_message.content:
                    print("SQL tool executed successfully. Setting data_retrieved=True.")
                    data_retrieved = True
                else:
                    print("SQL tool seems to have failed or returned no data.")
                    data_retrieved = False # Ensure it's False if SQL fails or returns nothing useful

        # Return the updated state, only modifying data_retrieved
        # Use **state syntax to return the whole state dictionary, only changing one key
        # Or just return the key to update:
        return {"data_retrieved": data_retrieved}

    # --- Graph Routing Logic ---
    # (Routing logic remains the same)

    def route_after_planning(self, state: AgentState) -> str:
        """Determines the next step after the LLM plans an action."""
        print("--- ROUTING AFTER PLANNING ---")
        last_message = state["messages"][-1]
        if isinstance(last_message, AIMessage) and last_message.tool_calls:
            print("======after planning, is ai message=================")
            if state["user_confirmation"] == "yes":
                print("Routing to execute tool")
                return "execute_tool"
            else:
                print("Routing to END (AI provided direct response or clarification)")
                return END
        else:
            print("Routing to END (AI provided direct response or clarification)")
            return END

    def route_after_confirmation(self, state: AgentState) -> str:
        """Determines the next step after user confirmation."""
        print("--- ROUTING AFTER CONFIRMATION ---")
        user_confirmation = state.get("user_confirmation")
        if user_confirmation == "yes":
            print("Routing to Execute Tool (ToolNode)")
            return "execute_tool"
        elif user_confirmation in ["no", "constraint_violation", "error_no_tool_call"]:
             # User rejected, constraint violation, or error -> Replan
             print(f"Routing back to Plan Action (Reason: {user_confirmation})")
             return "plan_action"
        else: # Should ideally not happen if confirmation node works correctly
             print("Routing to END (Unexpected confirmation state)")
             return END

    # Removed route_after_execution as ToolNode execution now flows directly to check_sql_success

    def route_after_tool_execution(self, state: AgentState) -> str:
        """Routes after tool execution (and potential state update). Always replan."""
        print("--- ROUTING AFTER TOOL EXECUTION & STATE UPDATE ---")
        print("Routing back to Plan Action")
        return "plan_action"


    # --- Graph Construction ---
    def _create_graph(self) -> StateGraph:
        """Create the LangGraph workflow."""
        workflow = StateGraph(AgentState)

        tool_node = ToolNode(self.tools)

        # Add nodes
        workflow.add_node("check_and_fetch_schema", self.check_initial_state)
        workflow.add_node("plan_action", self.plan_action)
        workflow.add_node("execute_tool", tool_node)
        workflow.add_node("check_sql_success", self.check_sql_success)

        # Set entry point
        workflow.set_entry_point("check_and_fetch_schema")
        workflow.add_edge("check_and_fetch_schema", "plan_action")

        # Define edges
        workflow.add_conditional_edges(
            "plan_action",
            self.route_after_planning,
            {"execute_tool": "execute_tool", END: END}
        )

        # After ToolNode executes, check if it was SQL and update state
        workflow.add_edge("execute_tool", "check_sql_success")

        # After checking SQL success (or skipping if not SQL), always replan
        workflow.add_edge("check_sql_success", "plan_action")

        # Compile the graph *with the checkpointer*
        return workflow.compile(
            checkpointer=self.memory,
            interrupt_after=["plan_action"]
        ) # Pass the MemorySaver instance here

