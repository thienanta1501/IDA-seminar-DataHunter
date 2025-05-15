"""Statistical analysis tools for the MCP Server.

This module provides tools for performing statistical analysis on CSV datasets,
including calculating summary statistics (min, max, mean, std, etc.), generating
distribution and correlation plots, and exporting the results as an interactive
HTML report.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pandas.api.types import is_numeric_dtype, is_string_dtype, is_datetime64_any_dtype
import base64
from io import BytesIO
from typing import Dict, List, Optional, Tuple, Any, Union

# Set plot style
sns.set(style="whitegrid")

# --- Utility Functions ---

def plot_to_base64(plt_figure: plt.Figure) -> str:
    """Converts a Matplotlib figure to a base64 encoded PNG image string."""
    buf = BytesIO()
    plt_figure.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(plt_figure) # Close the figure to free memory
    return f"data:image/png;base64,{img_str}"

# --- HTML Generation Functions ---

def generate_html_header(title: str = "Data Analysis Report") -> str:
    """Generates the basic HTML header with some styling."""
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: sans-serif; margin: 20px; line-height: 1.6; }}
        h1, h2, h3 {{ color: #333; border-bottom: 1px solid #eee; padding-bottom: 5px; }}
        h2 {{ margin-top: 30px; }}
        .column-section {{ border: 1px solid #ddd; padding: 15px; margin-bottom: 20px; border-radius: 5px; background-color:#f9f9f9; }}
        .stats-table {{ border-collapse: collapse; width: auto; margin-bottom: 15px; }}
        .stats-table th, .stats-table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        .stats-table th {{ background-color: #f2f2f2; }}
        .plot-container {{ text-align: center; margin-top: 15px; margin-bottom: 15px; }}
        .plot-container img {{ max-width: 90%; height: auto; border: 1px solid #ccc; }}
        .missing-pie {{ max-width: 300px; }} /* Smaller size for pie chart */
        pre {{ background-color: #eee; padding: 10px; border-radius: 3px; overflow-x: auto; }}
        .correlation-matrix img {{ max-width: 100%; height: auto; border: 1px solid #ccc; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
"""

def generate_html_footer() -> str:
    """Generates the HTML footer."""
    return """
</body>
</html>
"""

def generate_column_html(
    col_name: str,
    col_type: str,
    missing_count: int,
    missing_rate: float,
    stats_html: str,
    dist_plot_base64: Optional[str],
    missing_pie_base64: str
) -> str:
    """Generates the HTML block for a single column's analysis."""
    html = f"""
    <div class="column-section">
        <h3>Column: {col_name}</h3>
        <p><strong>Identified Type:</strong> {col_type}</p>
        <h4>Missing Values</h4>
        <p>Count: {missing_count} ({missing_rate:.2f}%)</p>
        <div class="plot-container">
            <img src="{missing_pie_base64}" alt="Missing Values Pie Chart" class="missing-pie">
        </div>
        <h4>Statistics</h4>
        {stats_html}
        <h4>Distribution</h4>
    """
    if dist_plot_base64:
        html += f"""
        <div class="plot-container">
            <img src="{dist_plot_base64}" alt="Distribution Plot">
        </div>
        """
    else:
        html += "<p>No distribution plot generated (e.g., constant value, unsupported type, or error).</p>"

    html += "</div>" # Close column-section
    return html

def generate_correlation_html(corr_plot_base64: Optional[str]) -> str:
    """Generates the HTML block for the correlation matrix."""
    html = """
    <h2>Overall Numerical Feature Correlation</h2>
    """
    if corr_plot_base64:
        html += f"""
        <div class="plot-container correlation-matrix">
             <p>Pearson Correlation Matrix:</p>
            <img src="{corr_plot_base64}" alt="Correlation Matrix">
        </div>
        """
    else:
        html += "<p>Correlation matrix not generated (less than 2 numerical features).</p>"
    return html


# --- Analysis & Plotting Functions (Modified for HTML Output) ---

# Use identify_column_types and read_data from previous functional example (no changes needed)
# (Assuming they are defined elsewhere or copied here)
# ... (read_data, identify_column_types functions go here) ...
# --- 1. Data Reading and Standardization Functions --- (Copied from previous)

def read_data(filepath: str) -> pd.DataFrame:
    """Reads data from CSV or Excel file."""
    print(f"--- Reading Data from: {filepath} ---")
    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath)
    elif filepath.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(filepath)
    else:
        raise ValueError(f"Unsupported file format: {filepath}. Please use CSV or Excel.")
    print(f"Successfully read data. Shape: {df.shape}")
    print("-" * 30)
    return df

def identify_column_types(
    df: pd.DataFrame,
    date_cols: Optional[List[str]] = None,
    cat_threshold: int = 20,
    id_cols: Optional[List[str]] = None
) -> Tuple[pd.DataFrame, Dict[str, List[str]]]:
    """
    Identifies column types (numerical, categorical, datetime, other) and
    attempts to convert specified/detected date columns.

    Returns:
        Tuple[pd.DataFrame, Dict[str, List[str]]]: A tuple containing:
            - The DataFrame with potential dtype corrections (esp. datetime, category).
            - A dictionary mapping type names to lists of column names.
    """
    print("--- Identifying Column Types ---")
    df_processed = df.copy() # Work on a copy
    date_cols = date_cols if date_cols else []
    id_cols = id_cols if id_cols else []

    col_types: Dict[str, List[str]] = {
        "numerical": [],
        "categorical": [],
        "datetime": [],
        "id": list(id_cols), # Start with specified IDs
        "other": [],
    }

    # Handle explicit date columns first
    for col in date_cols:
        if col in df_processed.columns:
            try:
                df_processed[col] = pd.to_datetime(df_processed[col], errors='coerce')
                if not df_processed[col].isnull().all():
                    col_types["datetime"].append(col)
                else:
                    print(f"Warning: Column '{col}' specified as date could not be fully converted. Treating as object.")
                    if col not in col_types["id"]: col_types["other"].append(col)
            except Exception as e:
                print(f"Warning: Could not convert column '{col}' to datetime: {e}. Treating as object.")
                if col not in col_types["id"]: col_types["other"].append(col)
        else:
            print(f"Warning: Specified date column '{col}' not found in DataFrame.")

    # Process remaining columns
    for col in df_processed.columns:
        print(col, df_processed[col].dtype)
        if col in col_types["datetime"] or col in col_types["id"]:
            continue
        
        # Attempt datetime auto-detection for object columns
        if is_string_dtype(df_processed[col]):
            print("string but datetime")
            try:
                sample = df_processed[col].dropna().iloc[:100]
                if len(sample) > 0:
                    temp_converted = pd.to_datetime(sample, errors='coerce')
                    # Heuristic: check if conversion looks reasonable
                    if not temp_converted.isnull().all() and temp_converted.dt.year.nunique() > 0:
                        # print(f"Attempting auto-conversion of column '{col}' to datetime.") # Less verbose for report gen
                        converted_col = pd.to_datetime(df_processed[col], errors='coerce')
                        if not converted_col.isnull().all():
                             df_processed[col] = converted_col
                             col_types["datetime"].append(col)
                             continue # Move to next column
                        # else:
                            # print(f"Auto-conversion of '{col}' to datetime failed, keeping as object.")
            except Exception:
                 pass # Ignore errors during auto-detection attempt

        # Classify remaining columns
        if is_numeric_dtype(df_processed[col]):
            print("numeric")
            if len(df_processed[col].unique()) < cat_threshold and df_processed[col].dtype in ['int64', 'int32', 'int8']:
                 # print(f"Column '{col}' is numerical with few unique values (<{cat_threshold}). Treating as categorical.")
                 df_processed[col] = df_processed[col].astype('category')
                 col_types["categorical"].append(col)
            else:
                col_types["numerical"].append(col)

        elif is_string_dtype(df_processed[col]) or str(df_processed[col].dtype) == 'category':
            print("real string")
            nunique = df_processed[col].nunique(dropna=False)
            print(nunique, cat_threshold, len(df_processed))
            if (nunique <= cat_threshold) or (nunique < 0.5 * len(df_processed)):
                
                df_processed[col] = df_processed[col].astype('category')
                col_types["categorical"].append(col)
            elif nunique > 0.9 * len(df_processed) and col not in col_types["id"]: # Heuristic for potential ID
                # print(f"Column '{col}' has very high cardinality. Consider adding it to 'id_cols' if it's an identifier.")
                col_types["other"].append(col)
            else: # High-cardinality string/object
                 # print(f"Column '{col}' is string/object with > {cat_threshold} unique values. Treating as high-cardinality object/category (added to 'other').")
                 col_types["other"].append(col)
        elif is_datetime64_any_dtype(df_processed[col]):
             if col not in col_types["datetime"]: # Should be caught earlier
                 col_types["datetime"].append(col)
        elif col not in col_types["id"]: # Catch anything else not already classified
            nunique = df_processed[col].nunique(dropna=False)
            if (nunique <= cat_threshold) or (nunique < 0.5 * len(df_processed)):
                
                df_processed[col] = df_processed[col].astype('category')
                col_types["categorical"].append(col)
            elif nunique > 0.9 * len(df_processed) and col not in col_types["id"]: # Heuristic for potential ID
                # print(f"Column '{col}' has very high cardinality. Consider adding it to 'id_cols' if it's an identifier.")
                col_types["other"].append(col)
            else: # High-cardinality string/object
                 # print(f"Column '{col}' is string/object with > {cat_threshold} unique values. Treating as high-cardinality object/category (added to 'other').")
                 col_types["other"].append(col)

    print("\n--- Identified Column Types (for report generation) ---")
    # for type_name, cols in col_types.items():
    #     print(f"{type_name.capitalize()}: {cols}")
    # print("-" * 30)

    return df_processed, col_types


def plot_missing_pie(missing_count: int, total_count: int) -> str:
    """Generates a base64 pie chart for missing vs non-missing values."""
    if total_count == 0: return "" # Avoid division by zero
    non_missing_count = total_count - missing_count
    labels = ['Missing', 'Present']
    sizes = [missing_count, non_missing_count]
    colors = ['#ff9999','#66b3ff'] # Red for missing, Blue for present
    explode = (0.1, 0) if missing_count > 0 else (0, 0) # Explode 'Missing' slice if present

    fig, ax = plt.subplots(figsize=(3, 3)) # Small figure size
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
           shadow=False, startangle=90, textprops={'fontsize': 9})
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # plt.title('Missing Value Ratio', fontsize=10) # Title might be redundant in context
    return plot_to_base64(fig)


def get_column_stats_html(series: pd.Series, col_type: str) -> str:
    """Generates HTML representation of statistics for a column."""
    stats_html = "<p>No statistics generated.</p>" # Default
    if col_type == "numerical":
        try:
            desc = series.describe()
            skewness = series.skew()
            kurt = series.kurt()
            stats_df = pd.DataFrame({
                'Value': [
                    f"{desc['count']:.0f}", f"{desc['mean']:.3f}", f"{desc['std']:.3f}",
                    f"{desc['min']:.3f}", f"{desc['25%']:.3f}", f"{desc['50%']:.3f}",
                    f"{desc['75%']:.3f}", f"{desc['max']:.3f}", f"{skewness:.3f}", f"{kurt:.3f}"
                ]
            }, index=[
                'Count', 'Mean', 'Std Dev', 'Min', '25%', 'Median (50%)', '75%', 'Max', 'Skewness', 'Kurtosis'
            ])
            stats_html = stats_df.to_html(classes='stats-table', header=False, border=0)
        except Exception as e:
            stats_html = f"<p>Error calculating numerical stats: {e}</p>"

    elif col_type == "categorical":
        try:
            counts = series.value_counts()
            freq = series.value_counts(normalize=True)
            stats_df = pd.DataFrame({
                'Count': counts,
                'Frequency (%)': freq.apply(lambda x: f"{x:.2%}")
            }).head(10) # Show top 10 categories
            stats_df.index.name = 'Category'
            stats_html = f"<p>Value Counts (Top {len(stats_df)}):</p>" + stats_df.to_html(classes='stats-table', border=0)
            stats_html += f"<p>Unique Values: {series.nunique()}</p>"
        except Exception as e:
            stats_html = f"<p>Error calculating categorical stats: {e}</p>"

    elif col_type == "datetime":
        try:
            desc = series.describe(datetime_is_numeric=True) # Treat datetime like numeric for describe
            stats_df = pd.DataFrame({
                'Value': [
                    f"{desc['count']:.0f}", f"{desc['min']}", f"{desc['max']}"
                 ]
            }, index=['Count', 'Min Date', 'Max Date'])
            stats_html = stats_df.to_html(classes='stats-table', header=False, border=0)
            stats_html += f"<p>Unique Values: {series.nunique()}</p>"
        except Exception as e:
            # Fallback if datetime describe fails
            try:
                 stats_html = f"<p>Count: {series.count()}<br>Unique: {series.nunique()}<br>Min: {series.min()}<br>Max: {series.max()}</p>"
            except Exception as e2:
                 stats_html = f"<p>Error calculating datetime stats: {e2}</p>"

    elif col_type == "other" or col_type == "id":
         try:
             stats_html = f"<p>Count: {series.count()}<br>Unique Values: {series.nunique()}</p>"
             if series.nunique() < 20: # Show top values if cardinality is low
                  counts = series.value_counts()
                  freq = series.value_counts(normalize=True)
                  stats_df = pd.DataFrame({
                      'Count': counts,
                      'Frequency (%)': freq.apply(lambda x: f"{x:.2%}")
                  }).head(10)
                  stats_df.index.name = 'Value'
                  stats_html += "<p>Value Counts (Top 10):</p>" + stats_df.to_html(classes='stats-table', border=0)
         except Exception as e:
              stats_html = f"<p>Error calculating stats for 'other' type: {e}</p>"

    return stats_html


def plot_distribution(series: pd.Series, col_type: str, col_name: str, max_cat_plot: int = 15) -> Optional[str]:
    """Generates and returns base64 encoded distribution plot based on column type."""
    plot_base64 = None
    try:
        if series.nunique(dropna=False) <= 1:
             print(f"Skipping distribution plot for '{col_name}': constant value.")
             return None # Don't plot constant values

        if col_type == "numerical":
            fig, axes = plt.subplots(1, 2, figsize=(12, 4))
            fig.suptitle(f'Distribution of {col_name}', fontsize=14)
            # Histogram + KDE
            sns.histplot(series, kde=True, bins=30, ax=axes[0])
            skewness = series.skew()
            axes[0].set_title(f'Histogram + KDE\nSkewness: {skewness:.2f}')
            # Boxplot
            sns.boxplot(y=series, ax=axes[1])
            axes[1].set_title('Boxplot')
            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            plot_base64 = plot_to_base64(fig)

        elif col_type == "categorical":
            fig, ax = plt.subplots(figsize=(8, max(5, series.nunique()*0.3))) # Adjust height
            n_unique = series.nunique()
            data_to_plot = series
            plot_title = f'Frequency Distribution of {col_name}'

            if n_unique > max_cat_plot:
                top_cats = data_to_plot.value_counts().nlargest(max_cat_plot - 1).index
                plot_series = series.astype(str).apply(lambda x: x if x in top_cats else 'Other')
                data_to_plot = plot_series
                plot_title = f'Frequency Distribution (Top {max_cat_plot - 1} + Other)'

            order = data_to_plot.value_counts().index
            sns.countplot(y=data_to_plot, order=order, palette="viridis", ax=ax)
            ax.set_title(plot_title)
            plt.tight_layout()
            plot_base64 = plot_to_base64(fig)

        elif col_type == "datetime":
             if series.isnull().all():
                  print(f"Skipping datetime plot for '{col_name}': all nulls.")
                  return None
             temp_col = series.dropna() # Drop NaNs for plotting
             if temp_col.empty:
                  print(f"Skipping datetime plot for '{col_name}': no valid dates after dropping NaNs.")
                  return None

             fig, axes = plt.subplots(3, 1, figsize=(10, 12))
             fig.suptitle(f'Datetime Distribution of {col_name}', fontsize=14)

             if temp_col.dt.year.nunique() > 1:
                  sns.histplot(temp_col.dt.year, bins=min(30, temp_col.dt.year.nunique()), kde=False, ax=axes[0])
                  axes[0].set_title('Distribution by Year')
             else: axes[0].text(0.5, 0.5, 'Single Year', ha='center', va='center', transform=axes[0].transAxes); axes[0].set_title('Distribution by Year')

             if temp_col.dt.month.nunique() > 1:
                  sns.histplot(temp_col.dt.month, bins=12, kde=False, ax=axes[1])
                  axes[1].set_title('Distribution by Month'); axes[1].set_xticks(range(1,13))
             else: axes[1].text(0.5, 0.5, 'Single Month', ha='center', va='center', transform=axes[1].transAxes); axes[1].set_title('Distribution by Month')

             if temp_col.dt.dayofweek.nunique() > 1:
                  sns.histplot(temp_col.dt.dayofweek, bins=7, kde=False, ax=axes[2])
                  axes[2].set_title('Distribution by Day of Week'); axes[2].set_xticks(range(7)); axes[2].set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
             else: axes[2].text(0.5, 0.5, 'Single Day of Week', ha='center', va='center', transform=axes[2].transAxes); axes[2].set_title('Distribution by Day of Week')

             plt.tight_layout(rect=[0, 0.03, 1, 0.95])
             plot_base64 = plot_to_base64(fig)

        # Add other types if needed (e.g., boolean)

    except Exception as e:
        print(f"Error plotting distribution for column '{col_name}': {e}")
        plt.close() # Ensure plot is closed on error
        plot_base64 = None # Indicate error

    return plot_base64


def plot_correlation_matrix(df: pd.DataFrame, numerical_cols: List[str]) -> Optional[str]:
    """Generates and returns base64 encoded correlation matrix plot."""
    plot_base64 = None
    valid_num_cols = [col for col in numerical_cols if col in df.columns and pd.api.types.is_numeric_dtype(df[col])]

    if len(valid_num_cols) < 2:
        print("Skipping Correlation Matrix plot (less than 2 numerical features).")
        return None

    try:
        corr_matrix = df[valid_num_cols].corr(method='pearson')
        fig_height = max(6, len(valid_num_cols) * 0.6)
        fig_width = max(8, len(valid_num_cols) * 0.8)
        fig, ax = plt.subplots(figsize=(fig_width, fig_height))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5, ax=ax)
        ax.set_title('Pearson Correlation Matrix (Numerical Features)')
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        plot_base64 = plot_to_base64(fig)
    except Exception as e:
        print(f"Error plotting correlation matrix: {e}")
        plt.close() # Ensure plot is closed on error
        plot_base64 = None

    return plot_base64


# --- Main Report Generation Function ---

def generate_html_report(
    data_source: str,
    date_cols: Optional[List[str]] = None,
    cat_threshold: int = 20,
    id_cols: Optional[List[str]] = None,
    report_title: str = "Data Analysis Report"
):
    """
    Performs analysis and generates a self-contained HTML report.

    Args:
        data_source: Path to data file (csv/excel).
        date_cols: List of column names to treat as datetime.
        cat_threshold: Max unique values for auto-categorical detection.
        id_cols: List of ID columns to exclude from detailed analysis.
        report_title: Title for the HTML report.
    """

    # 1. Load and prepare data
    if isinstance(data_source, str):
        df = read_data(data_source)
    else:
        raise ValueError("data_source must be a file path.")

    df_processed, column_types = identify_column_types(df, date_cols, cat_threshold, id_cols)
    total_rows = len(df_processed)

    # 2. Start HTML Document
    html_content = generate_html_header(report_title)
    html_content += f"<p>Dataset Shape: {df_processed.shape[0]} rows, {df_processed.shape[1]} columns</p>"
    html_content += "<h2>Column Analysis</h2>"

    # 3. Analyze and generate HTML for each column (excluding specified IDs)
    columns_to_analyze = [col for col in df_processed.columns if col not in column_types['id']]
    for col_name in columns_to_analyze:
        print(f"Analyzing column: {col_name}")
        series = df_processed[col_name]

        # Determine column type for analysis context
        col_type = "other" # Default
        for type_name, cols in column_types.items():
            if col_name in cols:
                col_type = type_name
                break

        # Missing values
        missing_count = series.isnull().sum()
        missing_rate = (missing_count / total_rows) * 100 if total_rows > 0 else 0
        missing_pie_base64 = plot_missing_pie(missing_count, total_rows)

        # Statistics
        stats_html = get_column_stats_html(series, col_type)

        # Distribution Plot
        dist_plot_base64 = plot_distribution(series, col_type, col_name)

        # Append column HTML
        html_content += generate_column_html(
            col_name, col_type, missing_count, missing_rate,
            stats_html, dist_plot_base64, missing_pie_base64
        )

    # 4. Generate Correlation Matrix HTML
    corr_plot_base64 = plot_correlation_matrix(df_processed, column_types["numerical"])
    html_content += generate_correlation_html(corr_plot_base64)

    # 5. Finalize HTML
    html_content += generate_html_footer()

    # 6. Save HTML file
    try:
        # with open(output_html_file, 'w', encoding='utf-8') as f:
        #     f.write(html_content)
        return html_content
    except Exception as e:
        return f"Error generating report: {e}"

