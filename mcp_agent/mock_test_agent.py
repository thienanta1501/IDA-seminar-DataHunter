from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from typing import Type, Optional, Any, Dict
class SQLToolInput(BaseModel):
    query: str = Field(description="The SQL query to execute")

class VizToolInput(BaseModel):
    data_query: str = Field(description="SQL query to fetch data for visualization")
    plot_type: str = Field(description="Type of plot (e.g., bar, line, scatter)")
    x_column: str = Field(description="Column for x-axis")
    y_column: str = Field(description="Column for y-axis")

class MLToolInput(BaseModel):
    data_query: str = Field(description="SQL query to fetch data for ML model")
    model_type: str = Field(description="Type of ML model (e.g., linear_regression, decision_tree)")
    target_column: str = Field(description="Column to predict")
    feature_columns: list[str] = Field(description="List of feature columns")

def mock_get_db_structure() -> str:
    """Returns a mock database schema."""
    mock_schema = """
    Table: customers
    - id: INTEGER PRIMARY KEY
    - name: TEXT
    - email: TEXT
    - signup_date: DATE

    Table: orders
    - order_id: INTEGER PRIMARY KEY
    - customer_id: INTEGER
    - order_date: DATE
    - amount: FLOAT
    """
    return mock_schema

import json

def mock_sql_tool(query: str) -> str:
    """Simulates executing an SQL query and returns mock results."""
    if "select * from customers" in query.lower():
        return json.dumps([
            {"id": 1, "name": "Alice", "email": "alice@example.com", "signup_date": "2023-01-01"},
            {"id": 2, "name": "Bob", "email": "bob@example.com", "signup_date": "2023-02-01"}
        ])
    elif "select * from orders" in query.lower():
        return json.dumps([
            {"order_id": 101, "customer_id": 1, "order_date": "2023-03-01", "amount": 99.99},
            {"order_id": 102, "customer_id": 2, "order_date": "2023-03-15", "amount": 149.50}
        ])
    else:
        return json.dumps({"error": "Mock SQLTool: Query not recognized, please use SELECT * FROM customers or orders"})
    
def mock_visualize_tool(data_query: str, plot_type: str, x_column: str, y_column: str) -> str:
    """Simulates generating a visualization and returns a mock result."""
    mock_result = {
        "status": "success",
        "plot_type": plot_type,
        "data_query": data_query,
        "x_column": x_column,
        "y_column": y_column,
        "visualization": f"Mock {plot_type} plot generated with {x_column} on x-axis and {y_column} on y-axis."
    }
    return json.dumps(mock_result)

from typing import List

def mock_build_ml_model(data_query: str, model_type: str, target_column: str, feature_columns: List[str]) -> str:
    """Simulates training an ML model and returns a mock result."""
    mock_result = {
        "status": "success",
        "model_type": model_type,
        "data_query": data_query,
        "target_column": target_column,
        "feature_columns": feature_columns,
        "model_summary": f"Mock {model_type} model trained to predict {target_column} using features {', '.join(feature_columns)}."
    }
    return json.dumps(mock_result)