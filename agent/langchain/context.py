import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../mcp_server')))

from db.database import engine 
from sqlalchemy import MetaData

def get_schema() ->str:
    metadata = MetaData()
    metadata.reflect(bind=engine)
        
    # Description of database schema
    description = "Cấu trúc của cơ sở dữ liệu:\n"

    for table_name, table in metadata.tables.items():
        description += f"Bảng: {table_name}\n"
        for column in table.columns:
            description += f"- {column.name} ({column.type})"

            # Primary key
            if column.primary_key:
                description += " [PK]"

            # Foreign key
            for fk in column.foreign_keys:
                description += f" [FK → {fk.target_fullname}]"

            description += "\n"
        description += "\n"

    return description

if __name__ == "__main__":
    print(get_schema())