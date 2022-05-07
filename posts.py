from unittest import result
from db import db
import users
from flask import make_response

def feed():
    sql = "SELECT p.id, p.animals, p.city, p.timedate, p.comment, u.username FROM posts p, users u WHERE p.visible = True AND p.user_id=u.id ORDER BY p.timedate DESC"
    result = db.session.execute(sql)
    return result.fetchall()

def commentfeed(post_id):
    sql = "SELECT c.body, u.username, c.sent FROM comments c, users u WHERE c.user_id=u.id AND post_id=:post_id ORDER BY c.id"
    result = db.session.execute(sql, {"post_id":post_id})
    return result.fetchall()

def forum_commentfeed(forumpost_id):
    sql = "SELECT f.content, u.username, f.sent FROM forumcomments f, users u WHERE f.user_id=u.id AND forumpost_id=:forumpost_id ORDER BY f.id"
    result = db.session.execute(sql, {"forumpost_id":forumpost_id})
    return result.fetchall()

def post(animals,city,timedate,comment):
    user_id = users.get_my_id()
    sql = "INSERT INTO posts (user_id, animals, city, timedate, comment, visible) VALUES (:user_id, :animals, :city, :timedate, :comment, True)"
    db.session.execute(sql, {"user_id":user_id, "animals":animals, "city":city, "timedate":timedate, "comment":comment})
    db.session.commit()
    return True

def postforum(headline, content):
    user_id = users.get_my_id()
    sql = "INSERT INTO forumposts (user_id, headline, content, sent, visible) VALUES (:user_id, :headline, :content, NOW(), True)"
    db.session.execute(sql, {"user_id":user_id, "headline":headline, "content":content})
    db.session.commit()
    return True

def sendcomment(body, post_id):
    user_id = users.get_my_id()
    sql = "INSERT INTO comments (post_id, user_id, body, sent) VALUES (:post_id, :user_id, :body, NOW())"
    db.session.execute(sql, {"post_id":post_id, "user_id":user_id, "body":body})
    db.session.commit()
    return True

def commentforum(content,forumpost_id):
    user_id = users.get_my_id()
    sql = "INSERT INTO forumcomments (user_id, forumpost_id, content, sent) VALUES  (:user_id, :forumpost_id, :content, NOW())"
    db.session.execute(sql, {"user_id":user_id, "forumpost_id":forumpost_id, "content":content})
    db.session.commit()
    return True

def get_forum_post(id):
    sql = "SELECT f.headline, f.content, f.sent, u.username FROM forumposts f, users u WHERE f.user_id=u.id AND f.id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def forumfeed():
    sql = "SELECT f.id, f.headline, f.content, f.sent, u.username FROM forumposts f, users u WHERE f.user_id=u.id AND f.visible=True ORDER BY sent DESC"
    result = db.session.execute(sql)
    return result.fetchall()

def comment(body):
    sql = "INSERT INTO comments (post_id, user_id, body) VALUES ("

def search(query):
    sql = ("SELECT * FROM posts JOIN users ON (posts.user_id=users.id) WHERE posts.visible=True AND lower(posts.animals) LIKE lower(:query) OR lower(posts.city) LIKE lower(:query) OR users.username LIKE :query OR CAST(timedate AS text) like :query")
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    return result.fetchall()

def delete_post(id):
    sql = "UPDATE posts SET visible = False WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()
    return True

def delete_forum_post(id):
    sql = "UPDATE forumposts SET visible = False WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()
    return True

def get_post(id):
    sql = "SELECT p.id, p.animals, p.city, p.timedate, p.comment, u.username FROM posts p, users u WHERE p.user_id=u.id AND p.id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone() 

def get_forum_post(id):
    sql = "SELECT * FROM forumposts WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone() 

def get_user_posts(user_id):
    sql = "SELECT * FROM posts WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall() 