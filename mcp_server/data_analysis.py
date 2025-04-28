import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis
import io

# Hàm phân tích dataframe
def analyze_dataframe(df):
    analysis = {}

    # Dataset Shape
    analysis['shape'] = df.shape

    # Column Analysis
    column_analysis = []
    for col in df.columns:
        col_info = {}
        col_info['column_name'] = col

        # Identify type
        if pd.api.types.is_numeric_dtype(df[col]):
            col_info['type'] = 'numerical'
        elif pd.api.types.is_categorical_dtype(df[col]) or df[col].dtype == 'object':
            col_info['type'] = 'categorical'
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            col_info['type'] = 'datetime'
        else:
            col_info['type'] = 'unknown'

        # Missing values
        missing_count = df[col].isnull().sum()
        missing_percent = (missing_count / len(df)) * 100
        col_info['missing'] = {'count': missing_count, 'percent': missing_percent}

        # Statistic and Distribution
        if col_info['type'] == 'numerical':
            col_info['statistics'] = {
                'count': df[col].count(),
                'mean': df[col].mean(),
                'std_dev': df[col].std(),
                'min': df[col].min(),
                '25%': df[col].quantile(0.25),
                'median': df[col].median(),
                '75%': df[col].quantile(0.75),
                'max': df[col].max(),
                'skewness': skew(df[col].dropna()),
                'kurtosis': kurtosis(df[col].dropna())
            }
        elif col_info['type'] == 'categorical':
            value_counts = df[col].value_counts() # Lấy top 5 giá trị phổ biến nhất
            col_info['statistics'] = {
                'value_counts': value_counts.to_dict(),  # Chuyển thành dictionary
                'unique_values': df[col].nunique()
            }
        elif col_info['type'] == 'datetime':
            col_info['statistics'] = {
                'count': df[col].count(),
                'unique': df[col].nunique(),
                'min': df[col].min(),
                'max': df[col].max()
            }

        column_analysis.append(col_info)

    analysis['columns'] = column_analysis

    # Overall Numerical Feature Correlation
    numerical_cols = df.select_dtypes(include=np.number).columns
    if len(numerical_cols) > 1:
        correlation_matrix = df[numerical_cols].corr(method='pearson')
        analysis['correlation_matrix'] = correlation_matrix  # Giữ lại ma trận nếu cần
        analysis['correlation_heatmap'] = plot_correlation_heatmap(correlation_matrix)  # Heatmap

    return analysis

# Hàm vẽ biểu đồ
def plot_distribution(df, col):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    sns.histplot(df[col], kde=True, ax=axes[0])
    axes[0].set_title(f"Histogram + KDE for {col}")
    sns.boxplot(x=df[col], ax=axes[1])
    axes[1].set_title(f"Boxplot for {col}")
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)
    return buf

def plot_categorical_distribution(df, col):
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.countplot(y=df[col], order=df[col].value_counts().index, ax=ax)
    ax.set_title(f"Frequency Distribution for {col}")
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)
    return buf

def plot_datetime_distribution(df, col):
    fig, axes = plt.subplots(1, 3, figsize=(18, 4))
    sns.histplot(df[col].dt.year, kde=False, ax=axes[0])
    axes[0].set_title(f"Year Distribution for {col}")
    sns.histplot(df[col].dt.month, kde=False, ax=axes[1])
    axes[1].set_title(f"Month Distribution for {col}")
    sns.histplot(df[col].dt.dayofweek, kde=False, ax=axes[2])
    axes[2].set_title(f"Day of Week Distribution for {col}")
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)
    return buf

def plot_correlation_heatmap(correlation_matrix):
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, ax=ax)
    ax.set_title("Correlation Heatmap", fontsize=16)
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)
    return buf