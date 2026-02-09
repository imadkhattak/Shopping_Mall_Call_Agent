import re


def fetching_schema():
    with open("Data/Imad_database.sql", "r", encoding="utf-8") as f:
        sql = f.read()

    tables = re.findall(
        r"CREATE TABLE\s+`?(\w+)`?\s*\(([\s\S]*?)\)\s*ENGINE",
        sql,
        re.IGNORECASE
    )

    schema = {}

    for table_name, body in tables:
        columns = []

        for line in body.splitlines():
            line = line.strip()

            # valid column lines start with `
            if line.startswith("`"):
                col = line.split()[0].strip("`,")
                columns.append(col)

        schema[table_name] = columns

    return schema



