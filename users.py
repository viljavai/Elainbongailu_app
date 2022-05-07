from unittest import result
from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username,password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = username
            return True
        else:
            return False

def logout():
    del session["user_id"]

def register(username,password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username,password)

def get_my_id():
    return session.get("user_id",0)

def get_user_id(username):
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    return result.fetchone()[0]

def get_my_username():
    return session.get("username")

def get_username(id):
    sql = "SELECT username FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def get_profile(user_id):
    sql = "SELECT p.description, p.favourite, u.username FROM profiles p, users u WHERE p.user_id=:user_id AND p.user_id = u.id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def edit_profile(description,favourite):
    user_id = get_my_id()
    sql = "INSERT INTO profiles (user_id, description, favourite) VALUES (:user_id, :description, :favourite)"
    db.session.execute(sql, {"user_id":user_id, "description":description, "favourite":favourite})
    db.session.commit()
    return True