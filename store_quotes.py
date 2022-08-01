import sqlite3 


app = sqlite3.connect("quotes.db")
cursor = app.cursor()
print("db is initialized")