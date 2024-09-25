CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  username VARCHAR(100) NOT NULL UNIQUE,
  email VARCHAR(200) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  PRIMARY KEY (id, username, email)
);

INSERT INTO users (name, username, email, password)
VALUE  ('John Doe', 'johndoe', 'johndoe@example.com', '123123');