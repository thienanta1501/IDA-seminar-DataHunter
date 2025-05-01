# streamlit_app: Chatbot
import streamlit as st
import pandas as pd
import os
from PIL import Image
from client_main import ask_agent, handle_user_accept_tool
from agent import agent, thread
import asyncio
import io
import json

# --- Cấu hình giao diện chính ---
st.set_page_config(page_title="Chatbot", page_icon="💬", layout="wide")

# --- Tuỳ chỉnh giao diện sidebar ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        min-width: 300px;
        max-width: 75vw;
    }
    </style>
""", unsafe_allow_html=True)

# --- Hàm load file và dữ liệu ---
@st.cache_data
def load_table_files(directory):
    return [f for f in os.listdir(directory) if f.endswith(".csv")]

@st.cache_data
def load_dataframe(file_path):
    return pd.read_csv(file_path)

def check_for_changes(directory, key):
    current_files = set(os.listdir(directory))
    if key not in st.session_state:
        st.session_state[key] = current_files
    if current_files != st.session_state[key]:
        st.session_state[key] = current_files
        return True
    return False

# --- Sidebar ---
st.sidebar.title("📊 Analysis Results")
tab_selection = st.sidebar.radio("Option", ["Chart", "Table"])

if st.sidebar.button("🔄 Reload Sidebar"):
    st.session_state.sidebar_updated = True

# --- Tab: Chart ---
if tab_selection == "Chart":
    if st.session_state.get("chart_data"):
        st.sidebar.subheader("📈 Chart List")
        for idx, chart in enumerate(st.session_state.chart_data):
            st.sidebar.image(chart, use_container_width=True, caption=f"Chart {idx + 1}")
            buffer = io.BytesIO()
            chart.save(buffer, format="PNG")
            st.sidebar.download_button(
                label=f"⬇️ Download chart {idx + 1}",
                data=buffer.getvalue(),
                file_name=f"chart_{idx + 1}.png",
                mime="image/png"
            )
    else:
        st.sidebar.info("📭 No charts yet. Send a request!")

# --- Tab: Table ---
elif tab_selection == "Table":
    if st.session_state.get("table_data"):
        st.sidebar.subheader("📋 Table List")
        for idx, table in enumerate(st.session_state.table_data):
            st.sidebar.write(f"*Table {idx + 1}*")
            st.sidebar.dataframe(table)
            csv_buffer = io.StringIO()
            table.to_csv(csv_buffer, index=False)
            st.sidebar.download_button(
                label=f"⬇️ Download table {idx + 1}",
                data=csv_buffer.getvalue(),
                file_name=f"table_{idx + 1}.csv",
                mime="text/csv"
            )
    else:
        st.sidebar.info("📭 No tables yet. Send a request!")

# --- Logo và mô tả ---
st.image("logo.png", width=350)
st.write("Send a request to the chatbot and get your analysis results!")

# --- Hàm hiển thị message đẹp ---
def display_message(message, sender):
    if sender == "user":
        st.markdown(
            f"""
            <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
                <div style="background-color: #A5BFCC; padding: 10px; border-radius: 10px; max-width: 70%;">
                    <strong>You:</strong><br>{message}
                </div>
                <div style="margin-left: 10px;font-size: 40px">🧑‍💻</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">
                <div style="margin-right: 10px; font-size: 40px">👾</div>
                <div style="background-color: #A5BFCC; padding: 10px; border-radius: 10px; max-width: 70%;">
                    <strong>Assistant:</strong><br>{message}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# --- Lịch sử chat ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for user, bot, bot_mess in st.session_state.chat_history:
    display_message(user, "user")
    if isinstance(bot, pd.DataFrame):
        st.markdown("📋 Your table:")
        st.dataframe(bot)
    elif isinstance(bot, Image.Image):
        st.markdown("📊 Your chart:")
        st.image(bot, use_container_width=True)
    if bot_mess:
        display_message(bot_mess, "bot")

# --- Hàm chạy async ---
def run_async(func, *args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(func(*args))

def handle_yes_click():
    try:
        new_state = handle_user_accept_tool("yes", st.session_state.current_state)
        print(f"Chui vao yes")
        print(type(st.session_state.current_state))
        
        result = run_async(ask_agent, agent, st.session_state.last_user_input, thread, new_state)
        
        if isinstance(result, tuple) and len(result) == 4:
            bot_message, bot_response, response, _ = result
            
            if isinstance(bot_response, Image.Image):
                st.markdown("📊 Your chart:")
                st.image(bot_response, use_container_width=True)
                st.session_state.chart_data = st.session_state.get("chart_data", []) + [bot_response]
            elif isinstance(bot_response, str):
                try:
                    df = pd.DataFrame(json.loads(bot_response))
                    st.markdown("📋 Your table:")
                    st.dataframe(df)
                    st.session_state.table_data = st.session_state.get("table_data", []) + [df]
                    bot_response = df
                except Exception as e:
                    st.write(f"Error processing response: {e}")
            
            display_message(bot_message, "bot")
            st.session_state.chat_history.append((st.session_state.last_user_input, bot_response, bot_message))
        else:
            display_message("⚠️ Something went wrong after confirmation.", "bot")
    except Exception as e:
        st.write(f"Error in handle_yes_click: {e}")
    finally:
        st.session_state.waiting_confirmation = False

def handle_no_click():
    try:
        new_state = handle_user_accept_tool("no", st.session_state.current_state)
        
        result = run_async(ask_agent, agent, st.session_state.last_user_input, thread, new_state)
        
        if isinstance(result, tuple) and len(result) == 4:
            bot_response, _, _, _ = result
            display_message(bot_response, "bot")
            st.session_state.chat_history.append((st.session_state.last_user_input, None, bot_response))
        else:
            display_message("⚠️ Something went wrong after rejection.", "bot")
    except Exception as e:
        st.write(f"Error in handle_no_click: {e}")
    finally:
        st.session_state.waiting_confirmation = False

# --- Xử lý chat ---
user_input = st.chat_input("Send a request to the chatbot")

if user_input and not st.session_state.get("waiting_confirmation", False):
    state, next_action = run_async(ask_agent, agent, user_input, thread)
    display_message(user_input, "user")

    if next_action == "confirm":
        st.session_state.waiting_confirmation = True
        st.session_state.last_user_input = user_input
        st.session_state.current_state = state
        st.warning("⚠️ The assistant wants to use a tool. Do you allow it?")
        col1, col2 = st.columns(2)

        with col1:
            st.button("✅ Yes, proceed!", on_click=handle_yes_click, key="yes_button")

        with col2:
            st.button("❌ No, cancel!", on_click=handle_no_click, key="no_button")

    elif next_action == "end":
        result = run_async(ask_agent, agent, user_input, thread, state)
        if isinstance(result, tuple) and len(result) == 4:
            bot_message, bot_response, response, _ = result

            if isinstance(bot_response, Image.Image):
                st.markdown("📊 Your chart:")
                st.image(bot_response, use_container_width=True)
                st.session_state.chart_data = st.session_state.get("chart_data", []) + [bot_response]

            elif isinstance(bot_response, str):
                try:
                    df = pd.DataFrame(json.loads(bot_response))
                    st.markdown("📋 Your table:")
                    st.dataframe(df)
                    st.session_state.table_data = st.session_state.get("table_data", []) + [df]
                    bot_response = df
                except Exception:
                    pass

            display_message(bot_message, "bot")
            st.session_state.chat_history.append((user_input, bot_response, bot_message))
        else:
            display_message("⚠️ Something went wrong after action.", "bot")

# --- Reset Sidebar Flag ---
st.session_state.sidebar_updated = False
