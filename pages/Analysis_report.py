# streamlit_app: Báo cáo phân tích
import streamlit as st
import pandas as pd
from data_analysis import analyze_dataframe, plot_distribution, plot_categorical_distribution, plot_datetime_distribution
import io

st.set_page_config(page_title="Analysis Report", page_icon="📊", layout="wide")
st.title("📊 Analysis Report")

# --- CSS Sidebar tuỳ chỉnh ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        min-width: 300px;
        max-width: 75vw;
    }
    </style>
""", unsafe_allow_html=True)

# Khởi tạo session_state nếu chưa có
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "df" not in st.session_state:
    st.session_state.df = None
if "analysis" not in st.session_state:
    st.session_state.analysis = None

# Tải dữ liệu mẫu
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
if uploaded_file:
    st.session_state.uploaded_file = uploaded_file  # Lưu file vào session_state
    # Đọc file CSV từ buffer
    df = pd.read_csv(io.StringIO(uploaded_file.getvalue().decode("utf-8")))
    st.session_state.df = df # Lưu dataframe vào session_state
    st.session_state.analysis = analyze_dataframe(df)  # Lưu kết quả phân tích vào session_state
    
if st.session_state.uploaded_file:
    st.write("### Uploaded file:")
    st.write(f"**Name:** {st.session_state.uploaded_file.name}")
    st.write(f"**Size:** {st.session_state.uploaded_file.size} bytes")


# Sử dụng dữ liệu từ session_state nếu có
if st.session_state.analysis:
    analysis = st.session_state.analysis
    df = st.session_state.df

    # Dataset Shape
    st.subheader("Dataset Shape")
    st.write(f"Rows: {analysis['shape'][0]}, Columns: {analysis['shape'][1]}")

    # Column Analysis
    st.subheader("Column Analysis")
    for col in analysis['columns']:
        st.markdown(f"### Column: {col['column_name']}")
        st.write(f"Type: {col['type']}")
        st.write(f"Missing Values: {col['missing']['count']} ({col['missing']['percent']:.2f}%)")

        if col['type'] == 'numerical':
            st.write("Statistics:")
            st.table(pd.DataFrame([col['statistics']]))
            st.image(plot_distribution(df, col['column_name']), caption=f"Distribution for {col['column_name']}")
        elif col['type'] == 'categorical':
            st.write("Statistics:")
            st.table(pd.DataFrame.from_dict(col['statistics']['value_counts'], orient='index', columns=['Count']))
            st.image(plot_categorical_distribution(df, col['column_name']), caption=f"Frequency Distribution for {col['column_name']}")
        elif col['type'] == 'datetime':
            st.write("Statistics:")
            st.table(pd.DataFrame([col['statistics']]))
            st.image(plot_datetime_distribution(df, col['column_name']), caption=f"Datetime Distribution for {col['column_name']}")
   
    # Correlation Matrix
    # Hiển thị Correlation Heatmap
    if 'correlation_heatmap' in analysis:
        st.subheader("Overall Numerical Feature Correlation")
        st.image(analysis['correlation_heatmap'], caption="Correlation Heatmap")

# if uploaded_file:
#     df = pd.read_csv(uploaded_file)
#     analysis = analyze_dataframe(df)

#     # Dataset Shape
#     st.subheader("Dataset Shape")
#     st.write(f"Rows: {analysis['shape'][0]}, Columns: {analysis['shape'][1]}")

#     # Column Analysis
#     st.subheader("Column Analysis")
#     for col in analysis['columns']:
#         st.markdown(f"### Column: {col['column_name']}")
#         st.write(f"Type: {col['type']}")
#         st.write(f"Missing Values: {col['missing']['count']} ({col['missing']['percent']:.2f}%)")

#         if col['type'] == 'numerical':
#             st.write("Statistics:")
#             st.table(pd.DataFrame([col['statistics']]))
#             st.image(plot_distribution(df, col['column_name']), caption=f"Distribution for {col['column_name']}")
#         elif col['type'] == 'categorical':
#             st.write("Statistics:")
#             st.table(pd.DataFrame.from_dict(col['statistics']['value_counts'], orient='index', columns=['Count']))
#             st.image(plot_categorical_distribution(df, col['column_name']), caption=f"Frequency Distribution for {col['column_name']}")
#         elif col['type'] == 'datetime':
#             st.write("Statistics:")
#             st.table(pd.DataFrame([col['statistics']]))
#             st.image(plot_datetime_distribution(df, col['column_name']), caption=f"Datetime Distribution for {col['column_name']}")

#     # Correlation Matrix
#     # Hiển thị Correlation Heatmap
#     if 'correlation_heatmap' in analysis:
#         st.subheader("Overall Numerical Feature Correlation")
#         st.image(analysis['correlation_heatmap'], caption="Correlation Heatmap")