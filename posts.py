from db import db

def feed():
    sql = "SELECT * FROM posts"
    result = db.session.execute(sql)
    return result.fetchall()

def post(animals,city,timedate,comment):
    sql = "INSERT INTO posts (animals, city, timedate, comment) VALUES (:animals, :city, :timedate, :comment)"
    db.session.execute(sql, {"animals":animals, "city":city, "timedate":timedate, "comment":comment})
    db.session.commit()
    return True

def search(query):
    sql = "SELECT * FROM posts WHERE animals LIKE :query OR city LIKE :query OR timedate LIKE :query"
    result = db.session.execute(sql, {"query":query})
    return result.fetchall()