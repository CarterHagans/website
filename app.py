from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import request,flash,redirect
from appcredientals import EMAIL,PASSWORD,RECEIVER,KEY
import smtplib,ssl


app = Flask(__name__)
app.secret_key = KEY

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/experience')
def experience():
    return render_template('experience.html')

@app.route('/contact/sent')
def contact_msg_sent():
    return render_template("msgsent.html")


@app.route('/contact' ,methods=["post","get"])
def contact():
    if request.method == "POST":
        author = request.form.get('email')
        message = request.form.get('message')
        msg_to_send =f"{author} has sent you a message! \nMessage content:\n{message}"
        context = ssl.create_default_context()
        port = 465
        with smtplib.SMTP_SSL("smtp.gmail.com",port,context=context) as server:
            server.login(EMAIL,PASSWORD)
            server.sendmail(EMAIL,RECEIVER,msg_to_send)
        return redirect("/contact/sent")
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