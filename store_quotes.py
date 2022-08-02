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


cursor.execute("""CREATE TABLE quote_tag(
        id INTEGER NOT NULL  PRIMARY KEY AUTOINCREMENT,
        quote_id INT ,
        tag_id INT ,
        FOREIGN KEY (quote_id) REFERENCES quote(quote_id) ON DELETE CASCADE ,
        FOREIGN KEY (tag_id) REFERENCES tag(tag_id) ON DELETE CASCADE
    );""")
print("quote_tag table created")


