"""Machine learning tools for the MCP Agent.

This module provides LangChain tools that interface with the MCP Server's
machine learning tools.
"""

from typing import Any, Dict, List, Optional, Union

#import aiohttp
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class MLModelInput(BaseModel):
    """Input for the machine learning model tool."""
    
    data: Union[Dict[str, Any], str] = Field(
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


class MLModelTool(BaseTool):
    """Tool for building machine learning models."""
    
    name = "build_ml_model"
    description = "Builds basic machine learning models (e.g., linear regression, decision trees) based on the provided data and parameters."
    args_schema = MLModelInput
    
    def __init__(self, server_url: str):
        """Initialize the tool.
        
        Args:
            server_url: URL of the MCP server.
        """
        super().__init__()
        self.server_url = server_url
    
    async def _arun(
        self,
        data: Union[Dict[str, Any], str],
        target_column: str,
        feature_columns: List[str],
        model_type: str,
        test_size: float = 0.2,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Run the tool asynchronously.
        
        Args:
            data: Data to use for training.
            target_column: Name of the target column.
            feature_columns: List of feature column names.
            model_type: Type of model to build.
            test_size: Fraction of data to use for testing.
            **kwargs: Additional tool arguments.
            
        Returns:
            The model output including performance metrics.
        """
        # async with aiohttp.ClientSession() as session:
        #     async with session.post(
        #         f"{self.server_url}/tools/build_ml_model",
        #         json={
        #             "data": data,
        #             "target_column": target_column,
        #             "feature_columns": feature_columns,
        #             "model_type": model_type,
        #             "test_size": test_size,
        #         },
        #     ) as response:
        #         result = await response.json()
        #         return result
        return {}
    def _run(
        self,
        data: Union[Dict[str, Any], str],
        target_column: str,
        feature_columns: List[str],
        model_type: str,
        test_size: float = 0.2,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Run the tool synchronously.
        
        Args:
            data: Data to use for training.
            target_column: Name of the target column.
            feature_columns: List of feature column names.
            model_type: Type of model to build.
            test_size: Fraction of data to use for testing.
            **kwargs: Additional tool arguments.
            
        Returns:
            The model output including performance metrics.
        """
        raise NotImplementedError("This tool only supports async execution") 