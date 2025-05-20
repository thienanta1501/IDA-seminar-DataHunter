"""Machine learning tools for the MCP Server.

This module provides tools for building and using machine learning models.
"""

from typing import Any, Dict, List, Optional, Union
import io
import numpy as np
import pandas as pd
from mcp.server.fastmcp import Context
from pydantic import BaseModel, Field
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor


class MLModelInput(BaseModel):
    """Input for the machine learning model tool."""
    
    data: Union[str] = Field(
        ...,
        description="Data to use for training, either as a DataFrame or a CSV string",
    )
    target_column: str = Field(
        ...,
        description="Name of the target column",
    )
    feature_columns: List[str] = Field(
        ...,
        description="List of feature column names",
    )
    model_type: str = Field(
        ...,
        description="Type of model to build (linear_regression or decision_tree)",
    )
    test_size: float = Field(
        default=0.2,
        description="Fraction of data to use for testing",
    )


class MLModelOutput(BaseModel):
    """Output from the machine learning model tool."""
    
    model_type: str = Field(..., description="Type of model that was built")
    r2_score: float = Field(..., description="R-squared score on the test set")
    mse: float = Field(..., description="Mean squared error on the test set")
    feature_importance: Dict[str, float] = Field(
        ...,
        description="Feature importance scores",
    )


async def build_ml_model(input_data: MLModelInput, ctx: Context) -> MLModelOutput:
    """Build a machine learning model.
    
    Args:
        input_data: The input data for the model.
        ctx: The MCP context.
        
    Returns:
        The model output including performance metrics.
    """
    # Parse the data if it's a string
    if isinstance(input_data.data, str):
        df = pd.read_csv(io.StringIO(input_data.data))
    else:
        df = input_data.data
    
    # Split features and target
    X = df[input_data.feature_columns]
    y = df[input_data.target_column]
    
    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=input_data.test_size, random_state=42
    )
    
    # Build the model
    if input_data.model_type.lower() == "linear_regression":
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        # Get feature importance (coefficients for linear regression)
        feature_importance = {
            col: abs(coef)
            for col, coef in zip(input_data.feature_columns, model.coef_)
        }
    
    elif input_data.model_type.lower() == "decision_tree":
        model = DecisionTreeRegressor(random_state=42)
        model.fit(X_train, y_train)
        
        # Get feature importance
        feature_importance = {
            col: imp
            for col, imp in zip(input_data.feature_columns, model.feature_importances_)
        }
    
    else:
        raise ValueError(f"Unsupported model type: {input_data.model_type}")
    
    # Make predictions and calculate metrics
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    
    return MLModelOutput(
        model_type=input_data.model_type,
        r2_score=r2,
        mse=mse,
        feature_importance=feature_importance,
    ) 