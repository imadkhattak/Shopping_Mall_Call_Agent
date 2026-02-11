import mysql.connector
from .agent import SQL_Query_Generator
from .config import host, port, password, user, database


connection = mysql.connector.connect(
    host=host,
    port=port,
    password=password,
    user=user,
    database=database
)

cursor = connection.cursor()

def Execute_Query(user_query):
    
    sql = SQL_Query_Generator(user_query)
    
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


