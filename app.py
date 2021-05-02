from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import request,flash,redirect
from appcredientals import EMAIL,PASSWORD,RECEIVER,KEY,ADMIN_PASSWORD
import smtplib,ssl
from datetime import datetime


app = Flask(__name__)
app.secret_key = KEY
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db.init_app(app)
activeRequest = "hello"


class PurchaseRequest(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(80))
    language = db.Column(db.String(100))
    RequestedCode = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self,email,language,RequestedCode):
        self.email = email
        self.language = language
        self.RequestedCode = RequestedCode


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

@app.route("/purchase")
def purchase():
    return render_template("purchase.html")

@app.route("/purchase/form",methods=["post","get"])
def purchase_form():
    if request.method == "POST":
        user_email = request.form.get("requestemail")
        language = request.form.get("requestlanguage")
        thing_to_code = request.form.get("RequestedCode")
        status = "Pending"
        data = PurchaseRequest(user_email,language,thing_to_code)
        db.session.add(data)
        db.session.commit()
        flash("Request sent!",'success')



    return render_template(("purchase_form.html"))

@app.route('/admin',methods=["post","get"])
def admin():
    if request.method == "POST":
        entered_password = request.form.get("enteredadminpassword")
        if entered_password == ADMIN_PASSWORD:
            return redirect("/admin/panel")
    return render_template("admin.html")

@app.route(f'/admin/<activeRequest>',methods=["post","get"])
def manage_request(activeRequest):
    selectedRequest  = PurchaseRequest.query.filter_by(id=activeRequest).first()
    if request.method == "GET":
        return render_template("manage.html",identification=selectedRequest.id,email=selectedRequest.email,language=selectedRequest.language,codeRequest=selectedRequest.RequestedCode,date=selectedRequest.date_created)
    if request.method == "POST":
        if request.form["deletebtn"]:
            db.session.delete(selectedRequest)
            db.session.commit()
            flash("Request has been deleted from the database.",'error')
        else:
            print("no")
        return render_template("manage.html",identification=selectedRequest.id,email=selectedRequest.email,language=selectedRequest.language,codeRequest=selectedRequest.RequestedCode,date=selectedRequest.date_created)

@app.route('/admin/panel',methods=["post","get"])
def admin_panel():
    if request.method == "POST":
        ID = request.form.get("projectID")
        global activeRequest
        activeRequest = ID
        return redirect(f"/admin/{activeRequest}",activeRequest)   
    if request.method == "GET":
        coderequests = PurchaseRequest.query.order_by(PurchaseRequest.date_created).all()
        return render_template("panel.html",coderequests=coderequests)


if __name__ == '__main__':
    app.run(debug=True)