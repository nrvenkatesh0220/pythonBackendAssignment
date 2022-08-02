import sqlite3 
import json
with open("quotes.json","r") as f:
    json_data = f.read()

def initialize_db():
    sqlConnection = sqlite3.connect("quotes.db")
    cursor = sqlConnection.cursor()    
    print("db is initialized")
    return cursor
cursor = initialize_db() 

python_data = json.loads(json_data)
quotes_list = python_data.get("quotes")
authors_list = python_data.get("authors")


cursor.execute("""CREATE TABLE author(
        author_id INTEGER NOT NULL  PRIMARY KEY AUTOINCREMENT,
        name VARCHAR ,
        born TEXT ,
        referece TEXT 
    )""") 
print("Author table created")


