import streamlit as st
import pandas as pd
import os
from PIL import Image
from test_mcp_server import ask_agent
import asyncio


# Thêm CSS để tùy chỉnh chiều rộng của sidebar
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        min-width: 300px; /* Đặt chiều rộng tối thiểu */
        max-width: 75vw; /* Đặt chiều rộng tối đa */
    }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_data
def load_table_files(directory):
    return [f for f in os.listdir(directory) if f.endswith(".csv")]

@st.cache_data
def load_dataframe(file_path):
    return pd.read_csv(file_path)

# --- Hàm kiểm tra thay đổi trong thư mục ---
def check_for_changes(directory, key):
    current_files = set(os.listdir(directory))
    if key not in st.session_state:
        st.session_state[key] = current_files
    if current_files != st.session_state[key]:
        st.session_state[key] = current_files
        return True
    return False

# --- Sidebar Tabs ---
st.sidebar.title("📊 Kết quả phân tích")
tab_selection = st.sidebar.radio("Chọn tab", options=["Biểu đồ", "Bảng dữ liệu"])

# --- Đường dẫn thư mục chứa file ---
chart_dir = "charts_data"
table_dir = "tables_data"

# Đảm bảo thư mục tồn tại
os.makedirs(chart_dir, exist_ok=True)
os.makedirs(table_dir, exist_ok=True)

# --- Lưu trữ danh sách file trong session state ---
if "chart_files" not in st.session_state:
    st.session_state.chart_files = [f for f in os.listdir(chart_dir) if f.endswith((".png", ".jpg"))]

if "table_files" not in st.session_state:
    st.session_state.table_files = [f for f in os.listdir(table_dir) if f.endswith(".csv")]

# --- Tab: Biểu đồ ---
if tab_selection == "Biểu đồ":
    if check_for_changes(chart_dir, "chart_files"):
        st.session_state.chart_files = [f for f in os.listdir(chart_dir) if f.endswith((".png", ".jpg"))]

    if st.session_state.chart_files:
        st.sidebar.subheader("📈 Danh sách biểu đồ")
        for chart_file in st.session_state.chart_files:
            st.sidebar.markdown(f"**🖼 {chart_file}**")
            image = Image.open(os.path.join(chart_dir, chart_file))
            st.sidebar.image(image, use_container_width=True)

            with open(os.path.join(chart_dir, chart_file), "rb") as img_file:
                st.sidebar.download_button("⬇️ Tải biểu đồ", img_file, file_name=chart_file)
    else:
        st.sidebar.info("📭 Chưa có biểu đồ nào. Gửi yêu cầu để tạo biểu đồ!")

# --- Tab: Bảng dữ liệu ---
elif tab_selection == "Bảng dữ liệu":
    # Kiểm tra thay đổi trong thư mục
    if check_for_changes(table_dir, "table_files"):
        st.session_state.table_files = [f for f in os.listdir(table_dir) if f.endswith(".csv")]

    # Hiển thị danh sách bảng dữ liệu
    if st.session_state.table_files:
        st.sidebar.subheader("📋 Danh sách bảng dữ liệu")
        for table_file in st.session_state.table_files:
            st.sidebar.markdown(f"**📄 {table_file}**")
            # Sử dụng st.cache_data để tránh tải lại không cần thiết
            df = load_dataframe(os.path.join(table_dir, table_file))
            st.sidebar.dataframe(df.head(10))  # Hiển thị tối đa 10 dòng

            with open(os.path.join(table_dir, table_file), "rb") as csv_file:
                st.sidebar.download_button("⬇️ Tải bảng", csv_file, file_name=table_file)
    else:
        st.sidebar.info("📭 Chưa có bảng dữ liệu nào. Gửi yêu cầu để sinh dữ liệu!")

# --- Giao diện Chat bên phải ---
st.image("logo.png", width=350)
st.write("Nhập câu hỏi hoặc yêu cầu của bạn vào khung bên dưới:")

# Lưu trữ lịch sử chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Hiển thị các đoạn chat cũ
for user, bot in st.session_state.chat_history:
    st.chat_message("user").write(user)
    st.chat_message("assistant").write(bot)

# Input người dùng
user_input = st.chat_input("Nhập yêu cầu ở đây")

def run_async(func, *args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(func(*args))

if user_input:
    bot_response = run_async(ask_agent, user_input)

    st.session_state.chat_history.append((user_input, bot_response))
    st.chat_message("user").write(user_input)
    st.chat_message("assistant").write(bot_response)
