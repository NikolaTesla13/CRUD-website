from flask import Flask, render_template, url_for, request
from datetime import datetime
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS notes (
    name TEXT,
    date_created TEXT
    )""")

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        task_content = request.form['content']
        cursor.execute("INSERT INTO notes VALUES (?, ?)", (task_content, 'now'))
    cursor.execute("SELECT rowid,* FROM notes")
    return render_template('index.html', tasks=cursor.fetchall())


@app.route('/delete/<int:id>')
def delete(id):
    cursor.execute("DELETE FROM notes WHERE rowid = ?", (id,))
    conn.commit()
    cursor.execute("SELECT rowid,* FROM notes")
    return render_template('index.html', tasks=cursor.fetchall())

@app.route('/update/<int:id>/<string:content>', methods=['POST', 'GET'])
def update(id, content):
    if request.method == 'POST':
        task_content = request.form['content']
        cursor.execute("""UPDATE notes SET name = ?
                WHERE rowid = ?
        """, (task_content,id))
        conn.commit()
        return index()
    else:
        return render_template('update.html', id=id, content=content)

if __name__ == "__main__":
    app.run(debug=True)

conn.commit()
conn.close()