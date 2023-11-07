import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
import flask
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

con = sqlite3.connect("users.db", check_same_thread=False)
cur = con.cursor()

def apology(message, route):
    if route == 'index':
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
            return apology("Escribe un usuario.", "index")

        password = request.form.get("password")
        if not password:
            return apology("Escribe una contraseña.", "index")

        user  = cur.execute("SELECT hash, type FROM users WHERE username = ?", (username,)).fetchone()
        if not user or not check_password_hash(user[0], password):
            return apology("Usuario o contraseña equivocado.", "index")
        elif user[1] == "admin":
            users  = cur.execute("SELECT * FROM users WHERE type = 'usuario'").fetchall()
            print(users)
            return render_template("teacher.html", users=users)
        else:
            return render_template("student.html")
    
    else:
        return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        usertype = request.form.get("usertype") 

        if not username or not password:
            return apology("Usuario y contraseña requerido.", "register")

        existing_user = cur.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
        if existing_user:
           return apology("Nombre de usuario ya usado.", "register")

        if not confirmation == password:
           return apology("Contraseñas no concuerdan", "register")

        hashed_password = generate_password_hash(password)

        cur.execute("INSERT INTO users (username, hash, type) VALUES (?, ?, ?)", (username, hashed_password, usertype))
        con.commit()

        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/delete_user", methods=["POST"])
def delete_user():
	if not request.method == "POST":
		return redirect("/")
	id = request.form.get("id")
	cur.execute("DELETE FROM users WHERE id = ?", (id,))
	con.commit()
	users = cur.execute("SELECT * FROM users WHERE type = 'usuario'")
	return render_template("teacher.html", users=users)

@app.route("/edit_username", methods=["POST"])
def edit_username():
	if not request.method == "POST":
		return redirect("/")
	username = request.form.get("username")
	id = request.form.get("id")
	cur.execute("UPDATE users SET username = ? WHERE id = ?", (username, id))
	con.commit()
	users = cur.execute("SELECT * FROM users WHERE type = 'usuario'")
	return render_template("teacher.html", users=users)
	



