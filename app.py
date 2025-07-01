from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('fest.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, name TEXT, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS participants (id INTEGER PRIMARY KEY, name TEXT, email TEXT, event_id INTEGER)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        conn = sqlite3.connect('fest.db')
        conn.execute("INSERT INTO events (name, date) VALUES (?, ?)", (name, date))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    return render_template('add_event.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    conn = sqlite3.connect('fest.db')
    events = conn.execute("SELECT * FROM events").fetchall()
    conn.close()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        event_id = request.form['event']
        conn = sqlite3.connect('fest.db')
        conn.execute("INSERT INTO participants (name, email, event_id) VALUES (?, ?, ?)", (name, email, event_id))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))

    return render_template('register.html', events=events)

@app.route('/participants')
def participants():
    conn = sqlite3.connect('fest.db')
    rows = conn.execute('''SELECT p.name, p.email, e.name as event_name 
                           FROM participants p JOIN events e ON p.event_id = e.id''').fetchall()
    conn.close()
    return render_template('participants.html', participants=rows)

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
