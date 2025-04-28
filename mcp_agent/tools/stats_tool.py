import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import (
    LabelEncoder,
    OneHotEncoder,
    StandardScaler,
    MinMaxScaler,
    PolynomialFeatures,
    KBinsDiscretizer,
)
from sklearn.feature_selection import mutual_info_regression, mutual_info_classif
from sklearn.impute import SimpleImputer
from pandas.api.types import is_numeric_dtype, is_string_dtype, is_datetime64_any_dtype
from typing import Dict, List, Optional, Tuple, Any, Union

# Set plot style
sns.set(style="whitegrid")

# --- 1. Data Reading and Standardization Functions ---

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
        if col in col_types["datetime"] or col in col_types["id"]:
            continue

        # Attempt datetime auto-detection for object columns
        if is_string_dtype(df_processed[col]):
            try:
                sample = df_processed[col].dropna().iloc[:100]
                if len(sample) > 0:
                    temp_converted = pd.to_datetime(sample, errors='coerce')
                    # Heuristic: check if conversion looks reasonable
                    if not temp_converted.isnull().all() and temp_converted.dt.year.nunique() > 0:
                        print(f"Attempting auto-conversion of column '{col}' to datetime.")
                        converted_col = pd.to_datetime(df_processed[col], errors='coerce')
                        if not converted_col.isnull().all():
                             df_processed[col] = converted_col
                             col_types["datetime"].append(col)
                             continue # Move to next column
                        else:
                            print(f"Auto-conversion of '{col}' to datetime failed, keeping as object.")
            except Exception:
                 pass # Ignore errors during auto-detection attempt

        # Classify remaining columns
        if is_numeric_dtype(df_processed[col]):
            if len(df_processed[col].unique()) < cat_threshold and df_processed[col].dtype in ['int64', 'int32', 'int8']:
                 print(f"Column '{col}' is numerical with few unique values (<{cat_threshold}). Treating as categorical.")
                 df_processed[col] = df_processed[col].astype('category')
                 col_types["categorical"].append(col)
            else:
                col_types["numerical"].append(col)
        elif is_string_dtype(df_processed[col]) or str(df_processed[col].dtype) == 'category':
            nunique = df_processed[col].nunique(dropna=False)
            if nunique <= cat_threshold:
                df_processed[col] = df_processed[col].astype('category')
                col_types["categorical"].append(col)
            elif nunique > 0.9 * len(df_processed) and col not in col_types["id"]: # Heuristic for potential ID
                print(f"Column '{col}' has very high cardinality. Consider adding it to 'id_cols' if it's an identifier.")
                col_types["other"].append(col)
            else: # High-cardinality string/object
                 print(f"Column '{col}' is string/object with > {cat_threshold} unique values. Treating as high-cardinality object/category (added to 'other').")
                 col_types["other"].append(col)
        elif is_datetime64_any_dtype(df_processed[col]):
             if col not in col_types["datetime"]: # Should be caught earlier
                 col_types["datetime"].append(col)
        elif col not in col_types["id"]: # Catch anything else not already classified
             print(f"Column '{col}' has unhandled type: {df_processed[col].dtype}. Treating as 'other'.")
             col_types["other"].append(col)

    print("\n--- Identified Column Types ---")
    for type_name, cols in col_types.items():
        print(f"{type_name.capitalize()}: {cols}")
    print("-" * 30)

    return df_processed, col_types

def calculate_missing_info(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates missing value counts and rates for each column."""
    print("--- Calculating Missing Values ---")
    missing_count = df.isnull().sum()
    missing_rate = (missing_count / len(df)) * 100
    missing_df = pd.DataFrame({
        'Missing Count': missing_count,
        'Missing Rate (%)': missing_rate,
        'Data Type': df.dtypes
    })
    missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values(by='Missing Rate (%)', ascending=False)
    if not missing_df.empty:
        print(missing_df)
    else:
        print("No missing values found.")
    print("-" * 30)
    return missing_df


# --- 2. General Statistics Function ---

def get_general_statistics(df: pd.DataFrame, column_types: Dict[str, List[str]]) -> Optional[pd.DataFrame]:
    """Calculates and prints descriptive statistics for numerical and categorical features."""
    print("\n--- General Statistics ---")
    desc_num_df = None

    # Numerical Features
    if column_types["numerical"]:
        print("\nNumerical Features:")
        num_cols = column_types["numerical"]
        desc_num = df[num_cols].describe().T
        desc_num['skewness'] = df[num_cols].skew()
        desc_num['kurtosis'] = df[num_cols].kurt()
        print(desc_num)
        desc_num_df = desc_num # Save for potential return
    else:
        print("\nNo numerical features identified.")

    # Categorical Features
    if column_types["categorical"]:
        print("\nCategorical Features (Top 5 Frequencies):")
        cat_cols = column_types["categorical"]
        for col in cat_cols:
            print(f"\n--- {col} ---")
            # Check if column still exists and is categorical
            if col in df.columns and str(df[col].dtype) == 'category':
                 print(df[col].value_counts(normalize=True).head().apply(lambda x: f"{x:.2%}"))
                 print(f"Total Unique Values: {df[col].nunique()}")
            elif col in df.columns:
                 print(f"(Info: Column '{col}' type might have changed, currently {df[col].dtype})")
                 print(df[col].value_counts(normalize=True).head().apply(lambda x: f"{x:.2%}"))
                 print(f"Total Unique Values: {df[col].nunique()}")
            else:
                 print(f"(Info: Column '{col}' not found)")
    else:
        print("\nNo low-cardinality categorical features identified.")

    print("-" * 30)
    return desc_num_df # Return numerical stats df


# --- 3. Visualization Functions ---

def _plot_numerical(df: pd.DataFrame, col: str):
    """Helper function to plot distribution for a single numerical column."""
    plt.figure(figsize=(12, 5))
    plt.suptitle(f'Distribution Analysis for: {col}', fontsize=14)

    # Histogram + KDE
    plt.subplot(1, 2, 1)
    sns.histplot(df[col], kde=True, bins=30)
    skewness = df[col].skew()
    plt.title(f'Histogram + KDE\nSkewness: {skewness:.2f}')
    plt.xlabel(col)
    plt.ylabel('Frequency')

    # Boxplot
    plt.subplot(1, 2, 2)
    sns.boxplot(y=df[col])
    plt.title('Boxplot (Outliers & Variance)')
    plt.ylabel(col)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

def _plot_categorical(df: pd.DataFrame, col: str, max_cat_plot: int):
    """Helper function to plot distribution for a single categorical column."""
    plt.figure(figsize=(10, 6))
    plt.suptitle(f'Categorical Analysis for: {col}', fontsize=14)
    n_unique = df[col].nunique()

    data_to_plot = df[col]
    plot_title = 'Frequency Distribution'

    if n_unique > max_cat_plot:
        print(f"Grouping less frequent categories in '{col}' for plotting (>{max_cat_plot} unique).")
        top_cats = data_to_plot.value_counts().nlargest(max_cat_plot - 1).index
        # Use .loc to avoid SettingWithCopyWarning if data_to_plot was a slice
        plot_series = df[col].astype(str).apply(lambda x: x if x in top_cats else 'Other')
        # Ensure 'Other' is treated as a category if needed, convert back for plotting
        # data_to_plot = pd.Series(plot_series, name=col) # Create a new series
        data_to_plot = plot_series # Use the modified series directly
        plot_title = f'Frequency Distribution (Top {max_cat_plot - 1} + Other)'


    # Calculate order based on frequency
    order = data_to_plot.value_counts().index
    sns.countplot(y=data_to_plot, order=order, palette="viridis")
    plt.title(plot_title)
    plt.xlabel('Count')
    plt.ylabel(col)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

def _plot_datetime(df: pd.DataFrame, col: str):
    """Helper function to plot distribution for a single datetime column."""
    if df[col].isnull().all():
        print(f"Skipping visualization for '{col}' as it contains only null values.")
        return

    print(f"\n--- Analyzing {col} ---")
    try:
        # Ensure it's datetime
        if not pd.api.types.is_datetime64_any_dtype(df[col]):
            temp_col = pd.to_datetime(df[col], errors='coerce')
            if temp_col.isnull().all():
                 print(f"Could not convert '{col}' to datetime for plotting.")
                 return
        else:
            temp_col = df[col]


        plt.figure(figsize=(12, 10))
        plt.suptitle(f'Datetime Analysis for: {col}', fontsize=14)

        # Plot by Year
        plt.subplot(3, 1, 1)
        if temp_col.dt.year.nunique() > 1:
            sns.histplot(temp_col.dt.year, bins=min(30, temp_col.dt.year.nunique()), kde=False)
            plt.title(f'{col} - Distribution by Year')
            plt.xlabel('Year')
        else:
            plt.text(0.5, 0.5, 'Only one year present', ha='center', va='center', transform=plt.gca().transAxes)
            plt.title(f'{col} - Distribution by Year (Single Year)')

        # Plot by Month
        plt.subplot(3, 1, 2)
        if temp_col.dt.month.nunique() > 1:
            sns.histplot(temp_col.dt.month, bins=12, kde=False)
            plt.title(f'{col} - Distribution by Month')
            plt.xlabel('Month')
            plt.xticks(range(1, 13))
        else:
            plt.text(0.5, 0.5, 'Only one month present', ha='center', va='center', transform=plt.gca().transAxes)
            plt.title(f'{col} - Distribution by Month (Single Month)')

        # Plot by Day of Week
        plt.subplot(3, 1, 3)
        if temp_col.dt.dayofweek.nunique() > 1:
            sns.histplot(temp_col.dt.dayofweek, bins=7, kde=False)
            plt.title(f'{col} - Distribution by Day of Week')
            plt.xlabel('Day of Week (0=Mon, 6=Sun)')
            plt.xticks(range(7), ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
        else:
            plt.text(0.5, 0.5, 'Only one day of week present', ha='center', va='center', transform=plt.gca().transAxes)
            plt.title(f'{col} - Distribution by Day of Week (Single Day)')

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()

    except Exception as e:
        print(f"Could not plot datetime feature '{col}'. Error: {e}")


def visualize_distributions(df: pd.DataFrame, column_types: Dict[str, List[str]], max_cat_plot: int = 10):
    """Visualizes the distribution and variation of features based on their type."""
    print("\n--- Visualizing Distributions ---")

    # Numerical Variables
    print("\nNumerical Variable Distributions:")
    if not column_types["numerical"]:
        print("No numerical columns to visualize.")
    else:
        for col in column_types["numerical"]:
             if col in df.columns:
                  _plot_numerical(df, col)
             else:
                  print(f"Warning: Numerical column '{col}' not found in DataFrame for plotting.")


    # Categorical Variables
    print("\nCategorical Variable Distributions:")
    if not column_types["categorical"]:
        print("No low-cardinality categorical columns to visualize.")
    else:
        for col in column_types["categorical"]:
            if col in df.columns:
                 # Ensure column is treated as category/object for plotting
                 if pd.api.types.is_numeric_dtype(df[col]) and not pd.api.types.is_categorical_dtype(df[col]):
                      # If a numerical column was classified as categorical (low unique int)
                      # treat it as object for countplot purposes
                      _plot_categorical(df.assign(**{col: df[col].astype(str)}), col, max_cat_plot)
                 elif pd.api.types.is_categorical_dtype(df[col]) or pd.api.types.is_object_dtype(df[col]) or pd.api.types.is_string_dtype(df[col]):
                      _plot_categorical(df, col, max_cat_plot)
                 else:
                      print(f"Warning: Cannot plot categorical for column '{col}' with type {df[col].dtype}")
            else:
                 print(f"Warning: Categorical column '{col}' not found in DataFrame for plotting.")


    # Datetime Variables
    print("\nDatetime Variable Distributions:")
    if not column_types["datetime"]:
        print("No datetime columns to visualize.")
    else:
        for col in column_types["datetime"]:
            if col in df.columns:
                _plot_datetime(df, col)
            else:
                 print(f"Warning: Datetime column '{col}' not found in DataFrame for plotting.")

    print("-" * 30)


# --- 4. Relationship Analysis Functions ---

def analyze_correlations(df: pd.DataFrame, numerical_cols: List[str], corr_threshold: float = 0.7):
    """Calculates and visualizes Pearson and Spearman correlations for numerical columns."""
    print("\n--- Analyzing Correlations (Numerical Features) ---")
    if len(numerical_cols) < 2:
        print("Skipping Correlation Matrix (less than 2 numerical features).")
        return

    valid_num_cols = [col for col in numerical_cols if col in df.columns and pd.api.types.is_numeric_dtype(df[col])]
    if len(valid_num_cols) < 2:
        print("Skipping Correlation Matrix (less than 2 valid numerical features found).")
        return

    # Pearson Correlation
    print("\nCorrelation Matrix (Pearson):")
    corr_matrix_pearson = df[valid_num_cols].corr(method='pearson')
    plt.figure(figsize=(max(8, len(valid_num_cols)*0.8), max(6, len(valid_num_cols)*0.6)))
    sns.heatmap(corr_matrix_pearson, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
    plt.title('Pearson Correlation Matrix')
    plt.show()

    # Spearman Correlation
    print("\nCorrelation Matrix (Spearman):")
    corr_matrix_spearman = df[valid_num_cols].corr(method='spearman')
    plt.figure(figsize=(max(8, len(valid_num_cols)*0.8), max(6, len(valid_num_cols)*0.6)))
    sns.heatmap(corr_matrix_spearman, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
    plt.title('Spearman Correlation Matrix')
    plt.show()

    # Highlight highly correlated pairs
    highly_correlated = corr_matrix_pearson.abs().unstack()
    highly_correlated = highly_correlated[highly_correlated > corr_threshold]
    highly_correlated = highly_correlated[highly_correlated < 1.0]
    highly_correlated = highly_correlated.drop_duplicates()
    if not highly_correlated.empty:
        print(f"\nPairs with Absolute Pearson Correlation > {corr_threshold}:")
        print(highly_correlated)
    else:
        print(f"\nNo pairs found with Absolute Pearson Correlation > {corr_threshold}.")


def analyze_categorical_vs_target(df: pd.DataFrame, categorical_cols: List[str], target_col: str):
    """Performs Crosstabs and Chi-squared tests for categorical features against a categorical target."""
    print(f"\n--- Analyzing Categorical Features vs Categorical Target '{target_col}' ---")
    if not target_col in df.columns or target_col not in categorical_cols:
         print(f"Error: Target column '{target_col}' not found or not identified as categorical.")
         return

    for col in categorical_cols:
        if col != target_col and col in df.columns:
             print(f"\n--- {col} vs {target_col} ---")
             # Ensure both columns are suitable (e.g., categorical or object)
             if not (pd.api.types.is_categorical_dtype(df[col]) or pd.api.types.is_object_dtype(df[col])):
                 print(f"Skipping '{col}': Not categorical or object type.")
                 continue
             try:
                 # Crosstab
                 crosstab = pd.crosstab(df[col], df[target_col], normalize='index')
                 print("Crosstab (Normalized by row):")
                 print(crosstab.applymap(lambda x: f"{x:.2%}"))

                 # Chi-squared Test
                 contingency_table = pd.crosstab(df[col], df[target_col])
                 if contingency_table.shape[0] < 2 or contingency_table.shape[1] < 2:
                      print("Chi-squared Test: Skipped (requires at least 2 categories in both variables).")
                      continue

                 chi2, p, dof, expected = stats.chi2_contingency(contingency_table)
                 print(f"Chi-squared Test: Chi2={chi2:.2f}, p-value={p:.3f}")
                 print(" -> Significant association detected (p < 0.05)" if p < 0.05 else " -> No significant association detected (p >= 0.05)")
             except ValueError as e:
                 print(f"Could not compute crosstab/chi2. Error: {e}")
             except Exception as e:
                 print(f"An unexpected error occurred during crosstab/chi2. Error: {e}")
        elif col == target_col:
            pass # Don't compare target with itself
        else:
            print(f"Warning: Categorical column '{col}' not found.")


def analyze_numerical_vs_target(df: pd.DataFrame, numerical_cols: List[str], target_col: str):
    """Performs ANOVA F-tests for numerical features against a categorical target."""
    print(f"\n--- Analyzing Numerical Features vs Categorical Target '{target_col}' ---")
    if not target_col in df.columns or not (pd.api.types.is_categorical_dtype(df[target_col]) or pd.api.types.is_object_dtype(df[target_col])):
         print(f"Error: Target column '{target_col}' not found or not identified as categorical/object.")
         return

    valid_num_cols = [col for col in numerical_cols if col in df.columns]

    for col in valid_num_cols:
        print(f"\n--- {col} vs {target_col} ---")
        # Prepare data for ANOVA: list of arrays, one for each group, handling NaNs
        groups_data = [group_df[col].dropna() for _, group_df in df.groupby(target_col, observed=True) if not group_df[col].isnull().all()]
        # Filter out groups with less than 2 samples (or customize this threshold)
        groups_data = [g for g in groups_data if len(g) >= 2]

        if len(groups_data) >= 2:
            try:
                f_value, p_value = stats.f_oneway(*groups_data)
                print(f"ANOVA F-test: F={f_value:.2f}, p-value={p_value:.3f}")
                print("   -> Significant difference in means detected (p < 0.05)" if p_value < 0.05 else "   -> No significant difference in means detected (p >= 0.05)")
            except ValueError as e: # e.g., zero variance within groups
                print(f"   Could not perform ANOVA for '{col}'. Error: {e}")
            except Exception as e:
                 print(f"   An unexpected error occurred during ANOVA for '{col}'. Error: {e}")
        else:
            print(f"   Skipping ANOVA for '{col}' (requires at least 2 groups with >= 2 non-NaN values).")


def calculate_mutual_information(df: pd.DataFrame, column_types: Dict[str, List[str]], target_col: str) -> Optional[pd.Series]:
    """Calculates Mutual Information scores between features and the target."""
    print(f"\n--- Calculating Mutual Information vs Target '{target_col}' ---")
    if target_col not in df.columns:
        print(f"Error: Target column '{target_col}' not found.")
        return None

    df_mi = df.copy()
    features_for_mi = column_types["numerical"] + column_types["categorical"]
    if target_col in features_for_mi:
        features_for_mi.remove(target_col)

    valid_features = [f for f in features_for_mi if f in df_mi.columns]
    if not valid_features:
        print("No valid features found for MI calculation.")
        return None

    # Basic Imputation (median for numeric, mode/'Missing' for categorical)
    for col in valid_features:
         if col in column_types["numerical"] and df_mi[col].isnull().any():
             median_val = df_mi[col].median()
             df_mi[col] = df_mi[col].fillna(median_val)
             print(f"Imputed missing values in numerical '{col}' with median ({median_val:.2f}) for MI calc.")
         elif col in column_types["categorical"] and df_mi[col].isnull().any():
             mode_val = df_mi[col].mode()
             fill_value = mode_val[0] if not mode_val.empty else "Missing"
             # Ensure consistency: if 'Missing' wasn't a category, add it.
             if fill_value not in df_mi[col].cat.categories:
                 df_mi[col] = df_mi[col].cat.add_categories(fill_value)
             df_mi[col] = df_mi[col].fillna(fill_value)
             print(f"Imputed missing values in categorical '{col}' with '{fill_value}' for MI calc.")


    # Prepare features (X) and target (y)
    X_mi_list = []
    discrete_features_mask = []
    feature_names = []

    for col in valid_features:
         if col in column_types["categorical"]:
             # Use integer codes for MI
             X_mi_list.append(df_mi[col].cat.codes.values.reshape(-1, 1))
             discrete_features_mask.append(True)
             feature_names.append(col)
         elif col in column_types["numerical"]:
             X_mi_list.append(df_mi[col].values.reshape(-1, 1))
             discrete_features_mask.append(False)
             feature_names.append(col)

    if not X_mi_list:
         print("No features suitable for MI calculation after processing.")
         return None

    X_mi = np.hstack(X_mi_list)
    y_mi = df_mi[target_col]

    # Handle missing target values
    if y_mi.isnull().any():
        print("Warning: Target column has missing values. Excluding these rows from MI calculation.")
        not_null_idx = y_mi.notnull()
        X_mi = X_mi[not_null_idx, :]
        y_mi = y_mi[not_null_idx]

    if X_mi.shape[0] == 0 or len(y_mi) == 0:
        print("Insufficient data for MI calculation after handling missing target.")
        return None

    mi_scores = None
    try:
        # Determine target type for correct MI function
        if pd.api.types.is_numeric_dtype(y_mi) and not pd.api.types.is_bool_dtype(y_mi): # Treat non-bool numerical as regression
            print("Using mutual_info_regression for numerical target.")
            mi_scores = mutual_info_regression(X_mi, y_mi, discrete_features=discrete_features_mask, random_state=42)
        elif pd.api.types.is_categorical_dtype(y_mi) or pd.api.types.is_object_dtype(y_mi) or pd.api.types.is_bool_dtype(y_mi): # Treat categorical, object, bool as classification
            print("Using mutual_info_classif for categorical/boolean target.")
             # Target needs encoding if not already integer codes
            y_mi_encoded = LabelEncoder().fit_transform(y_mi)
            mi_scores = mutual_info_classif(X_mi, y_mi_encoded, discrete_features=discrete_features_mask, random_state=42)
        else:
            print(f"Target column '{target_col}' type ({y_mi.dtype}) not suitable for standard MI calculation.")
            return None

        mi_series = pd.Series(mi_scores, index=feature_names).sort_values(ascending=False)
        print("\nMutual Information Scores:")
        print(mi_series)
        print("-" * 30)
        return mi_series

    except Exception as e:
        print(f"Could not calculate Mutual Information. Error: {e}")
        print("-" * 30)
        return None

def generate_suggestions(
    df: pd.DataFrame,
    column_types: Dict[str, List[str]],
    missing_info: pd.DataFrame,
    target_col: Optional[str] = None,
    missing_threshold: float = 0.7,
    variance_threshold: float = 0.01,
    skewness_threshold: float = 1.0,
    corr_threshold: float = 0.7 # For target correlation check
    ) -> List[str]:
    """Generates suggestions based on data characteristics."""
    print("\n--- Data Suggestion Engine ---")
    suggestions = []

    # 1. High Missing Values
    if not missing_info.empty:
        high_missing = missing_info[missing_info['Missing Rate (%)'] > missing_threshold * 100]
        for col, row in high_missing.iterrows():
            suggestions.append(f"- Feature '{col}' has a very high missing rate ({row['Missing Rate (%)']:.2f}%). Consider removal or advanced imputation.")

    # 2. Low Variance (Numerical & Categorical)
    num_cols = [c for c in column_types["numerical"] if c in df.columns]
    if num_cols:
         num_vars = df[num_cols].var()
         low_variance_cols = num_vars[num_vars < variance_threshold]
         for col, var_val in low_variance_cols.items():
             suggestions.append(f"- Numerical feature '{col}' has very low variance ({var_val:.4f}). Consider removal.")

    cat_cols = [c for c in column_types["categorical"] if c in df.columns]
    for col in cat_cols:
        if df[col].nunique(dropna=False) <= 1:
            suggestions.append(f"- Categorical feature '{col}' has only one unique value (or only NaNs). Consider removal.")

    # 3. High Skewness (Numerical)
    if num_cols:
        num_skew = df[num_cols].skew()
        high_skew = num_skew[num_skew.abs() > skewness_threshold]
        for col, skew_val in high_skew.items():
            transform_suggestions = ["log (if positive)", "sqrt (if non-negative)"]
            # Check positivity for Box-Cox suggestion more carefully
            if (df[col].dropna() > 0).all():
                transform_suggestions.append("Box-Cox")
            suggestions.append(f"- Numerical feature '{col}' is highly skewed ({skew_val:.2f}). Consider transformations: {', '.join(transform_suggestions)}.")

    # 4. High Correlation with Target (if target exists and is numerical/suitable)
    if target_col and target_col in df.columns and target_col in num_cols:
        try:
            corrs = df[num_cols].corr(method='pearson') # Calculate fresh correlation matrix
            if target_col in corrs:
                corr_with_target = corrs[target_col].drop(target_col).abs().sort_values(ascending=False)
                strong_corr = corr_with_target[corr_with_target > corr_threshold]
                for col, corr_val in strong_corr.items():
                    suggestions.append(f"- Feature '{col}' has strong linear correlation ({corr_val:.2f}) with numerical target '{target_col}'.")

                # Check for multicollinearity among these high-correlation features
                strong_corr_cols = strong_corr.index.tolist()
                if len(strong_corr_cols) > 1:
                    sub_corr_matrix = df[strong_corr_cols].corr().abs()
                    upper_tri = sub_corr_matrix.where(np.triu(np.ones(sub_corr_matrix.shape, dtype=bool), k=1))
                    high_inter_corr = upper_tri[upper_tri > 0.8] # Threshold for inter-correlation
                    if not high_inter_corr.stack().empty: # Check if any values exist after stacking
                         suggestions.append(f"- High multicollinearity (>0.8) detected among features strongly correlated with the target ({strong_corr_cols}). Consider keeping only the most relevant or using dimensionality reduction.")
        except Exception as e:
             print(f"Could not calculate correlations for suggestions: {e}")

    # 5. High MI with Target (Could be added if MI scores are passed or recalculated)
    #    Requires passing the mi_series result from calculate_mutual_information

    # 6. Potential ID columns suggestion
    other_cols = [c for c in column_types["other"] if c in df.columns]
    for col in other_cols:
        if df[col].nunique(dropna=False) > 0.9 * len(df):
             suggestions.append(f"- Column '{col}' (Type 'other') has very high cardinality. If it's an identifier, add to `id_cols` during setup.")

    # Print Suggestions
    if suggestions:
        print("\nSuggestions:")
        for i, sugg in enumerate(suggestions):
            print(f"{i+1}. {sugg}")
    else:
        print("\nNo specific suggestions generated based on current thresholds.")

    print("-" * 30)
    return suggestions
