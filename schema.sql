CREATE TABLE posts (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users, animals TEXT NOT NULL, city TEXT NOT NULL, timedate DATE, comment TEXT, visible BOOLEAN);
CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT NOT NULL);
CREATE TABLE comments (id SERIAL PRIMARY KEY, post_id int REFERENCES posts, user_id INTEGER REFERENCES users, body text NOT NULL, sent TIMESTAMP);
CREATE TABLE forumposts (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users, headline TEXT, content TEXT, sent TIMESTAMP, visible BOOLEAN);
CREATE TABLE forumcomments (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users, forumpost_id INTEGER REFERENCES forumposts, content TEXT, sent TIMESTAMP, visible BOOLEAN);
CREATE TABLE profiles (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users, description TEXT, favourite TEXT);