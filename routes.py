from app import app
from flask import render_template, request, redirect, session
from os import getenv
import posts, users
from datetime import datetime
import db


@app.route("/")
def index():
    list = posts.feed()
    username = users.get_username()
    #image = posts.get_image()
    return render_template("index.html", posts=list, username=username)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="( ͡༎ຶ  ͜ʖ  ͡༎ຶ ) Väärä käyttäjätunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if len(username) > 25:
            return render_template("error.html", message="Valitse käyttäjätunnus, joka on alle 25 merkkiä!")
        if password1 != password2:
            return render_template("error.html", message="Kirjoitit salasanan väärin, yritä uudelleen!")
        if len(password1) < 6:
            return render_template("error.html", message="Salasanasi tulee olla vähintään 6 merkkiä pitkä!")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Käyttäjätunnus on jo käytössä!")

@app.route("/search")
def search():
    return render_template("searchform.html")

@app.route("/comment")
def comment():
    return render_template("comment.html")

@app.route("/send", methods=["POST"])
def send():
    animals = request.form["animals"]
    city = request.form["city"]
    timedate = request.form["timedate"]
    comment = request.form["comment"]
    if len(animals) > 50:
        return render_template("error.html", message="Syöte on liian pitkä!")
    if len(city) > 50:
        return render_template("error.html", message="Syöte on liian pitkä!")
    if len(comment) > 1000:
        return render_template("error.html", message="Syöte on liian pitkä!")
    if len(timedate) > 10:
        return render_template("error.html", message="Syöte on liian pitkä!")
    if posts.post(animals,city,timedate,comment):
        return redirect("/")

@app.route("/delete", methods=["GET "])
def delete():
    return render_template("delete.html")

#@app.route("/send", methods=["POST"])
#def send_image():
    #file = request.files["file"]
    #name = file.filename
    #if not name.endswith(".jpg"):
        #return "Kuvan pitää olla .jpg-muodossa!"
    #data = file.read()
    #if len(data) > 100*1024:
        #return "Tiedosto on liian suuri!"
    #if posts.post_image(file,name):
        #return redirect("/")
    #else:
        #return render_template("error.html", message="Postauksen lähetys ei onnistunut")

@app.route("/result")
def result():
    query = request.args["query"]
    results = posts.search(query)
    return render_template("result.html", resultlist=results)