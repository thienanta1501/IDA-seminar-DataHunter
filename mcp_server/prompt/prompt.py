
DB_INFORMATION_PROMPT = """
You are a helpful assistant that can answer questions about a database.
You are given a database schema and a question.
The database schema is a list of tables with their columns and data types with the following format:

==========
Table Name:
Columns:
- Column Name: Column Type - Column Description
Primary Key:
- Column Name
==========

Here is the database schema:
"""



def get_prompt(prompt_name: str) -> str:
    global DB_INFORMATION_PROMPT
    if prompt_name == "DB_INFORMATION_PROMPT":
        return DB_INFORMATION_PROMPT
    else:
        raise ValueError(f"Prompt {prompt_name} not found")

def save_prompt(prompt_name: str, prompt: str):
    global DB_INFORMATION_PROMPT
    if prompt_name == "DB_INFORMATION_PROMPT":
        DB_INFORMATION_PROMPT = prompt
    else:
        raise ValueError(f"Prompt {prompt_name} not found")
