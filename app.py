import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
import flask
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

con = sqlite3.connect("users.db")
cur = con.cursor()
def apology(message, route=None):
    if route:
        return render_template("index.html", message=message)
    else:
        return render_template("register.html", message=message)

@app.after_request
def after_request(response):        
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            return apology("Must provide a username", "index")

        password = request.form.get("password")
        if not password:
            return apology("Must provide a password", "index")

        rows = cur.execute("SELECT hash, type FROM users WHERE username = ?", username)
        rows.fetchall()
        if not rows or not check_password_hash(rows[0][0], password):
            return apology("Username or password not valid", "index")
        elif rows[1][0] == "teacher":
            return render_template("teacher.html")
        else:
            return render_template("student.html")
    
    else:
        return render_template("index.html")




