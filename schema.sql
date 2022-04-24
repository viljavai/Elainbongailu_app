CREATE TABLE posts (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users, animals TEXT NOT NULL, city TEXT NOT NULL, timedate DATE, comment TEXT, visible BOOLEAN);
CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT NOT NULL);
CREATE TABLE comments (id SERIAL PRIMARY KEY, post_id int REFERENCES posts, user_id INTEGER REFERENCES users, body text NOT NULL);
CREATE TABLE images (id SERIAL PRIMARY KEY, post_id int REFERENCES posts, name TEXT, data BYTEA);
CREATE TABLE likes (id SERIAL PRIMARY KEY, post_id int REFERENCES posts);