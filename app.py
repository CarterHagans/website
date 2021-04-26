from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/experience')
def experience():
    return render_template('experience.html')

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/experience/python")
def python():
    return render_template("python.html")

@app.route("/experience/JavaScript")
def JavaScript():
    return render_template("JavaScript.html")

@app.route("/experience/Lua")
def Lua():
    return render_template("lua.html")


if __name__ == '__main__':
    app.run(debug=True)