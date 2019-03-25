import os

from flask import Flask, request, render_template, \
     flash, session, url_for, redirect

from util import db


app = Flask(__name__)
app.secret_key = os.urandom(32)

#---------- Login Routes ----------
@app.route("/")
def login():
    if "logged_in" in session:
        return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/auth", methods=["POST"])
def authenticate():
    if db.auth_user(request.form["user"], request.form["password"]):
        session["logged_in"] = request.form["user"]
        return redirect(url_for("home"))
    else:
        flash("username or password is incorrect")
        return redirect(url_for("login"))

#---------- Register Routes ----------
@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/adduser", methods=["POST"])
def add_user():
    if(not request.form["user"].strip() or not request.form["password"] or not request.form["confirm_password"]):
        flash("Please fill in all fields")
        return redirect(url_for("register"))

    if(db.check_user(request.form["user"])):
        flash("User already exists")
        return redirect(url_for("register"))

    if(request.form["password"] != request.form["confirm_password"]):
        flash("Passwords don't match")
        return redirect(url_for("register"))

    db.add_user(request.form["user"], request.form["password"])
    session["logged_in"] = request.form["user"]
    return redirect(url_for("home"))

#---------- Logout Route ----------

@app.route("/logout")
def logout():
    try:
        session.pop("logged_in")
    finally:
        return redirect(url_for("login"))

@app.route("/home")
def home():
    prof = db.get_profile(session["logged_in"])
    print(prof[0])
    return render_template("home.html", user=session["logged_in"], name=prof[0], age=prof[1], score=prof[2])

@app.route("/edit")
def edit():
    return render_template("edit.html")

@app.route("/editProf")
def edit_prof():
    user = session["logged_in"]
    display = request.args["display"].encode("utf-8")
    age = request.args["age"]
    db.edit_profile(user, display, age)
    return redirect(url_for("home"))

if (__name__) == ("__main__"):
    app.debug = True
    app.run()
