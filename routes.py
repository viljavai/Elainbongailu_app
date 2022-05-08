from app import app
from flask import render_template, request, redirect, session
from os import getenv
import posts, users
from datetime import date
import db

#---------------------------------------------
# käyttäjätilien toiminnallisuus

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
            return render_template("error.html", message="Väärä käyttäjätunnus tai salasana")

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
        if len(username) > 20 or len(username) < 5:
            return render_template("error.html", message="Valitse käyttäjätunnus, joka on 5-20 merkkiä pitkä!")
        if password1 != password2:
            return render_template("error.html", message="Kirjoitit salasanan väärin, yritä uudelleen!")
        if len(password1) < 6 or len(password1) > 20:
            return render_template("error.html", message="Salasanasi tulee olla 6-20 merkkiä pitkä!")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Käyttäjätunnus on jo käytössä!")
#-------------------------------------------------------
# postaukset ja haku

@app.route("/")
def index():
    list = posts.feed()
    username = users.get_my_username()
    return render_template("index.html", posts=list, username=username)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/search")
def search():
    return render_template("searchform.html")

@app.route("/result")
def result():
    query = request.args["query"]
    results = posts.search(query)
    return render_template("result.html", resultlist=results)

@app.route("/comment/<int:id>")
def comment(id):
    post = posts.get_post(id)
    return render_template("comment.html", post=post)

@app.route("/comments/<int:id>")
def comments(id):
    commentfeed = posts.commentfeed(id)
    return render_template("commentfeed.html", commentfeed=commentfeed)

@app.route("/sendcomment/<int:id>", methods=["POST"])
def sendcomment(id):
    postid = id
    body = request.form["body"]
    if len(body) > 500:
        return render_template("error.html", message="Kommentin täytyy olla alle 500 merkkiä pitkä!")
    if posts.sendcomment(body,postid):
        return redirect("/")
    else:
        return render_template("error.html", message="Kommentin lähetys ei onnistunut!")

@app.route("/send", methods=["POST"])
def send():
    animals = request.form["animals"]
    city = request.form["city"]
    timedate = request.form["timedate"]
    comment = request.form["comment"]

    if len(animals) == 0 or len(city) == 0 or len(timedate) == 0:
        return render_template("error.html", message="Ethän jätä pakollisia kenttiä tyhjiksi!")
    if len(animals) > 50:
        return render_template("error.html", message="Syöte on liian pitkä!")
    if len(city) > 50:
        return render_template("error.html", message="Syöte on liian pitkä!")
    if len(comment) > 1000:
        return render_template("error.html", message="Syöte on liian pitkä!")
    if timedate < "1970-01-01" or timedate > str(date.today()):
        return render_template("error.html", message="Tarkasta päivämäärä!")

    try:
        posts.post(animals,city,timedate,comment)
        return redirect("/")
    except:
        return render_template("error.html", message="Syötäthän ajan oikeassa muodossa!")

@app.route("/delete/<int:id>", methods=["GET"])
def delete(id):
    post = posts.get_post(id)
    return render_template("delete.html", post=post)

@app.route("/deletepost/<int:id>", methods=["POST"])
def deletepost(id):
    postid = id
    if posts.delete_post(postid):
        return redirect("/")

#--------------------------------------
# profiilien toiminnallisuus

@app.route("/myprofile")
def myprofile():
    id = users.get_my_id()
    profile = users.get_profile(id)
    postlist = posts.get_user_posts(id)
    return render_template("myprofile.html", profiles=profile, postlist=postlist)

@app.route("/profile/<username>")
def profile(username):
    id = users.get_user_id(username)
    profile = users.get_profile(id)
    postlist = posts.get_user_posts(id)
    return render_template("profile.html", profiles=profile, postlist=postlist)

@app.route("/editprofile")
def editprofile():
    return render_template("editprofile.html")

@app.route("/sendprofile", methods=["POST"])
def sendprofile():
    description = request.form["description"]
    favourite = request.form["favourite"]

    if len(description) > 500:
        return render_template("error.html", message="Elämänkertasi on liian pitkä!")
    if len(favourite) > 100:
        return render_template("error.html", message="Valitse vähemmän lempieläimiä!")

    if users.edit_profile(description,favourite):
        return redirect("/myprofile")
    else:
        return render_template("error.html", message="Profiilin muokkaus ei onnistunut!")

#-------------------------------------------------
#foorumin toiminnallisuus

@app.route("/postforum", methods=["POST"])
def postforum():
    headline = request.form["headline"]
    content = request.form["content"]
    if len(content) < 5 or len(content) > 600:
        return render_template("error.html", message="Varmista että viesti ei ole tyhjä eikä yli 600 merkkiä pitkä!")
    if posts.postforum(headline,content):
        return redirect("/forum")

@app.route("/forum/<id>")
def commentforum(id):
    forumpost = posts.get_forum_post(id)
    return render_template("commentforum.html", forumpost=forumpost)

@app.route("/forumpostdetails/<int:id>")
def forumpostdetails(id):
    forumpost = posts.get_forum_post(id)
    comments = posts.forum_commentfeed(id)
    return render_template("forumpostdetails.html", forumpost=forumpost, comments=comments)

@app.route("/deleteforum/<int:id>")
def deleteforum(id):
    forumpost = posts.get_forum_post(id)
    return render_template("deleteforumpost.html", forumpost=forumpost)

@app.route("/deleteforumpost/<int:id>", methods=["POST"])
def deleteforumpost(id):
    postid = id
    if posts.delete_forum_post(postid):
        return redirect("/forum")

@app.route("/forum")
def forum():
    list = posts.forumfeed()
    return render_template("forum.html", forumposts=list)

@app.route("/newforumpost")
def newforumpost():
    return render_template("newforumpost.html")

@app.route("/postforumcomment/<id>", methods=["POST"])
def postforumcomment(id):
    forumid = id
    content = request.form["content"]
    if posts.commentforum(content,forumid):
        return redirect("/forum")
