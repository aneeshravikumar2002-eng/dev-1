from flask import Flask
import pymysql
import os

app = Flask(__name__)

db = pymysql.connect(
    host=os.environ.get("DB_HOST"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    database=os.environ.get("DB_NAME")
)

@app.route("/")
def home():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM news")
    rows = cursor.fetchall()

    output = "<h1>Latest News</h1>"

    for row in rows:
        output += f"<p>{row[1]}</p>"

    return output

app.run(host="0.0.0.0", port=5000)
