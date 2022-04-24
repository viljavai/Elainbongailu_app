from unittest import result
from db import db
import users
from flask import make_response

def feed():
    sql = "SELECT p.id, p.animals, p.city, p.timedate, p.comment, u.username FROM posts p, users u WHERE p.visible = True AND p.user_id=u.id ORDER BY p.timedate DESC"
    result = db.session.execute(sql)
    return result.fetchall()

def post(animals,city,timedate,comment):
    user_id = users.user_id()
    sql = "INSERT INTO posts (user_id, animals, city, timedate, comment, visible) VALUES (:user_id, :animals, :city, :timedate, :comment, True)"
    db.session.execute(sql, {"user_id":user_id, "animals":animals, "city":city, "timedate":timedate, "comment":comment})
    db.session.commit()
    return True

    #sql2 = "INSERT INTO images (name,data) VALUES (:name,:data)"
    #db.session.execute(sql2, {"name":name, "data":data})
    #db.session.commit()
    #return True

#def get_image():
    #sql = "SELECT data FROM images, posts WHERE images.post_id=:posts.id"
    #result = db.session.execute(sql, {"id":id})
    #data = result.fetchone()[0]
    #response = make_response(bytes(data))
    #response.headers.set("Content-Type", "image/jpeg")
    #return response

def comment(body):
    sql = "INSERT INTO comments (post_id, user_id, body) VALUES ("

def search(query):
    sql = ("SELECT * FROM posts JOIN users ON (posts.user_id=users.id) WHERE lower(posts.animals) LIKE lower(:query) OR lower(posts.city) LIKE lower(:query) OR users.username LIKE :query OR CAST(timedate AS text) like :query")
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    return result.fetchall()

def delete(id):
    sql = "SELECT * FROM posts WHERE id=:id"
    result = db.session.execute(sql)
    post = result.fetchone()

def get_post_id():
    sql = ""