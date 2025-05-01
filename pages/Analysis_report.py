import streamlit as st
import pandas as pd
from mcp_agent.tools.test import generate_html_report
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

# Tải dữ liệu mẫu
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(io.StringIO(uploaded_file.getvalue().decode("utf-8")))
    output_file = "analysis_report.html"
    analysis = generate_html_report(df, output_file) # Phân tích DataFrame thành HTML
    st.write("Analysis Report generated successfully!")
    # Hiển thị báo cáo HTML trong Streamlit
    with open(output_file, "r") as f:
        report_html = f.read()
    st.components.v1.html(report_html, height=800, scrolling=True)
    

