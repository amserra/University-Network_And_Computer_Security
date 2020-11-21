-- Initialize the database.
-- Drop any existing data and create empty tables (comment if you wish to keep data).

DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  emailVerified INTEGER NOT NULL DEFAULT 0
);
