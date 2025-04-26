import streamlit as st
import pandas as pd
import os
from PIL import Image
from test_mcp_server import ask_agent
import asyncio
import io
import json

# --- CSS Sidebar tuỳ chỉnh ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        min-width: 300px;
        max-width: 75vw;
    }
    </style>
""", unsafe_allow_html=True)

# --- Load file từ thư mục ---
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
st.sidebar.title("📊 Kết quả phân tích")
tab_selection = st.sidebar.radio("Chọn nội dung muốn hiển thị", ["Biểu đồ", "Bảng dữ liệu"])

if "sidebar_updated" not in st.session_state:
    st.session_state.sidebar_updated = False

if st.sidebar.button("🔄 Làm mới Sidebar"):
    st.session_state.sidebar_updated = True

# --- Tab: Biểu đồ ---
if tab_selection == "Biểu đồ":
    if "chart_data" in st.session_state and st.session_state.chart_data:
        st.sidebar.subheader("📈 Danh sách biểu đồ")
        for idx, chart in enumerate(st.session_state.chart_data):
            st.sidebar.image(chart, use_container_width=True, caption=f"Biểu đồ {idx + 1}")
            
            # Tạo buffer để lưu tạm hình ảnh
            image_buffer = io.BytesIO()
            chart.save(image_buffer, format="PNG")
            image_buffer.seek(0)

            # Nút tải biểu đồ
            st.sidebar.download_button(
                label=f"⬇️ Tải biểu đồ {idx + 1}",
                data=image_buffer,
                file_name=f"chart_{idx + 1}.png",
                mime="image/png"
            )
    else:
        st.sidebar.info("📭 Chưa có biểu đồ nào. Gửi yêu cầu để tạo biểu đồ!")

# --- Tab: Bảng dữ liệu ---
elif tab_selection == "Bảng dữ liệu":
    if "table_data" in st.session_state and st.session_state.table_data:
        st.sidebar.subheader("📋 Danh sách bảng dữ liệu")
        for idx, table in enumerate(st.session_state.table_data):
            st.sidebar.write(f"*Bảng {idx + 1}*")
            st.sidebar.dataframe(table)

            csv_buffer = io.StringIO()
            table.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()

            st.sidebar.download_button(
                label=f"⬇️ Tải bảng {idx + 1}",
                data=csv_data,
                file_name=f"table_{idx + 1}.csv",
                mime="text/csv"
            )
    else:
        st.sidebar.info("📭 Chưa có bảng dữ liệu nào. Gửi yêu cầu để sinh dữ liệu!")

# --- Giao diện chính ---
st.image("logo.png", width=350)
st.write("Nhập câu hỏi hoặc yêu cầu của bạn vào khung bên dưới:")

def display_message(message, sender):
    if sender == "user":
        st.markdown(
            f"""
            <div style="display: flex; justify-content: flex-end; align-items: flex-start; margin-bottom: 10px;">
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
            <div style="display: flex; justify-content: flex-start; align-items: flex-start; margin-bottom: 10px;">
                <div style="margin-right: 10px; font-size: 40px">👾</div>
                <div style="background-color: #A5BFCC; padding: 10px; border-radius: 10px; max-width: 70%;">
                    <strong>Assistant:</strong><br>{message}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# --- Lịch sử Chat ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for user, bot, bot_mess in st.session_state.chat_history:
    display_message(user, "user")
    
    # Kiểm tra xem bot có phải là DataFrame (bảng dữ liệu) không
    if isinstance(bot, pd.DataFrame):
        display_message("📋 Bảng dữ liệu của bạn:", "bot")
        st.dataframe(bot)  # Hiển thị bảng dữ liệu
        display_message(bot_mess, "bot")  # Hiển thị thông báo của bot

    # Nếu bot là hình ảnh (biểu đồ)
    elif isinstance(bot, Image.Image):
        display_message("📊 Biểu đồ của bạn:", "bot")
        st.image(bot, use_container_width=True)
        display_message(bot_mess, "bot")
    
    # Nếu bot là một thông điệp bình thường
    else:
        display_message(bot_mess, "bot")

# --- Xử lý Async ---
def run_async(func, *args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(func(*args))

# --- Input từ người dùng ---
user_input = st.chat_input("Nhập yêu cầu ở đây")

if user_input:
    bot_response, bot_message = run_async(ask_agent, user_input)

    st.session_state.chat_history.append((user_input, bot_response, bot_message))
    display_message(user_input, "user")

    if isinstance(bot_response, Image.Image):
        display_message("📊 Biểu đồ của bạn:", "bot")
        st.image(bot_response, use_container_width=True)

        if "chart_data" not in st.session_state:
            st.session_state.chart_data = []
        st.session_state.chart_data.append(bot_response)

    else:
        try:
            data_dict = json.loads(bot_response)
            df = pd.DataFrame(data_dict)
            st.chat_message("assistant").write("📋 Bảng dữ liệu của bạn:")
            st.dataframe(df)

            if "table_data" not in st.session_state:
                st.session_state.table_data = []
            st.session_state.table_data.append(df)

        except Exception:
            display_message(bot_message, "bot")
    
    display_message(bot_message, "bot")

# --- Reset trạng thái sidebar ---
if st.session_state.sidebar_updated:
    st.session_state.sidebar_updated = False
