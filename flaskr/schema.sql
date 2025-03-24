DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL
);

CREATE TABLE post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    author_id INTEGER,
    driver TEXT NOT NULL,
    sponsor TEXT NOT NULL,
    number INTEGER NOT NULL,
    year INTEGER NOT NULL,
    picture TEXT,  -- Optional field for the picture URL
    FOREIGN KEY (author_id) REFERENCES user(id)
);