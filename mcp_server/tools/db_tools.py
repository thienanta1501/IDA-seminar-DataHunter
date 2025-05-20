"""Database tools for the MCP Server.

This module provides tools for interacting with the PostgreSQL database.
"""

import io
from typing import Any, Dict, List, Optional, Union
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, inspect, text
from mcp_server.prompt.prompt import get_prompt, save_prompt
import os 
from dotenv import load_dotenv

load_dotenv()

def create_db_engine(connection_string: str):
    try:
        # Create SQLAlchemy engine
        engine = create_engine(connection_string)
        
        # Return connection
        return engine
    
    except SQLAlchemyError as e:
        raise SQLAlchemyError(f"Connection error: {str(e)}")
    
engine = None
def get_db_engine():
    global engine
    db_url = os.getenv("DATABASE_URL")
    if engine is None:
        engine = create_db_engine(connection_string=db_url)
    return engine

class SQLQueryInput(BaseModel):
    """Input for the SQL query tool."""
    
    query: str = Field(..., description="SQL query to execute")


class DBStructureOutput(BaseModel):
    """Output for the database structure tool."""
    
    schema: str = Field(..., description="Database schema as a string")


def get_db_structure(schema_name: str) -> DBStructureOutput:
    """Retrieve the PostgreSQL database schema using SQL and return it as a prompt.
    
    Args:
        engine: The SQLAlchemy engine object.
        schema_name: The name of the schema to inspect
        
    Returns:
        The database schema as a string.
    """
    DB_INFORMATION_PROMPT = get_prompt("DB_INFORMATION_PROMPT")

    try:
        # Query to get all tables in the specified schema
        tables_query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = '{schema}'
        """
        
        # Query to get column details for a specific table
        columns_query = """
        SELECT 
            cols.column_name, 
            cols.data_type, 
            pgd.description AS column_comment
        FROM 
            information_schema.columns cols
        LEFT JOIN 
            pg_catalog.pg_statio_all_tables as st 
            ON cols.table_schema = st.schemaname AND cols.table_name = st.relname
        LEFT JOIN 
            pg_catalog.pg_description pgd 
            ON pgd.objoid = st.relid AND pgd.objsubid = cols.ordinal_position
        WHERE 
            cols.table_schema = '{schema}' 
            AND cols.table_name = '{table_name}';

        """

        # Query to get the primary key for a specific table
        fk_query = """
        SELECT tc.constraint_name, kcu.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.constraint_column_usage kcu
        ON tc.constraint_name = kcu.constraint_name
        WHERE tc.table_schema = '{schema}'
        AND tc.table_name = '{table_name}'
        AND tc.constraint_type = 'PRIMARY KEY';"""
        
        # Initialize result dictionary
        schema_details = {}
        
        # Get all tables
        tables_query = tables_query.format(schema=schema_name)
        tables =  sql_tool(query=tables_query, is_server=True)
        
        # Iterate through each table
        # for table_name in tables_df['table_name']:
        for table in tables:
            DB_INFORMATION_PROMPT +=  "==========\n" + f"Table Name: {table['table_name']}\n" + "Columns:\n"
            
            # Get column details for the current table
            specific_columns_query = columns_query.format(schema=schema_name, table_name=table["table_name"])
            #print(specific_columns_query
            columns =  sql_tool(query=specific_columns_query,is_server=True)
            # Create dictionary of column names and their data types

            for row in columns:
                DB_INFORMATION_PROMPT += f"- {row['column_name']}: {row['data_type']} - {row['column_comment']}\n"

            
            # Get primary key for the current table
            fk_query = fk_query.format(schema=schema_name, table_name=table["table_name"])
            #fk_query_basemodel = SQLQueryInput(query=fk_query, return_format="dataframe")
            fk_df =  sql_tool(query=fk_query, is_server=True)
            DB_INFORMATION_PROMPT += "Primary Key:\n"
            for key in fk_df:
                DB_INFORMATION_PROMPT += f"- {key}\n"

        save_prompt("DB_INFORMATION_PROMPT", DB_INFORMATION_PROMPT)
        return DB_INFORMATION_PROMPT
    
    except SQLAlchemyError as e:
        raise SQLAlchemyError(f"Database error: {str(e)}")
    
    


def sql_tool(query: str,is_server = False) -> Union[str, str]:
    """Execute a SQL query on the PostgreSQL database.
    
    Args:
        query: the sql query that need to be execute
        
        
    Returns:
        The query results as a DataFrame or CSV string.
    """
    import json
    engine = get_db_engine()
    try:
        # Execute the query
        connection = engine.connect()
        result = connection.execute(text(query))

        if query.strip().upper().startswith('SELECT'):
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
        else:
            connection.commit()
            df = pd.DataFrame()
        connection.close()
        df = df.to_dict('records')
        return df
    except SQLAlchemyError as e:
        raise SQLAlchemyError(f"Database error: {str(e)}")
    