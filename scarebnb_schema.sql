CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email TEXT NOT NULL
    CHECK (position('@' IN email) > 1),
  username TEXT NOT NULL,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  bio TEXT,
  password TEXT NOT NULL,
  is_host BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE listings (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  location TEXT NOT NULL,
  description TEXT NOT NULL,
  price INTEGER NOT NULL,
  image_url TEXT NOT NULL,
  rating INTEGER NOT NULL,
  user_id INTEGER NOT NULL
    REFERENCES users ON DELETE CASCADE
);