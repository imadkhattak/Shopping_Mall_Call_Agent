import re
from pathlib import Path


def fetching_schema():

    with open("Data/Imad_database.sql", "r") as f:
        sql_content = f.read()


    table_matches = re.findall(r"CREATE TABLE\s+`?(\w+)`?\s*\((.*?)\);", sql_text, re.DOTALL | re.IGNORECASE)

    schema = {}

    for table_name, columns_str in table_matches:
        # Split columns by comma and clean
        columns = [col.strip() for col in columns_str.split(",") if col.strip()]
        schema[table_name] = columns

    # Print schema
    for table, cols in schema.items():
        print(f"Table: {table}")
        for col in cols:
            print(f"  - {col}")

            