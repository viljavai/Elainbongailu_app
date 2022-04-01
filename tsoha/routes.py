from app import app
from flask import render_template, request, redirect
import posts


@app.route("/")
def index():
    list = posts.feed()
    return render_template("index.html", posts=list)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/search")
def search():
    return render_template("searchform.html")

@app.route("/send", methods=["POST"])
def send():
    animals = request.form["animals"]
    city = request.form["city"]
    timedate = request.form["timedate"]
    comment = request.form["comment"]
    if posts.post(animals,city,timedate,comment):
        return redirect("/")

@app.route("/result")
def result():
    query = request.args["query"]
    results = posts.search(query)
    return render_template("result.html", resultlist=results)