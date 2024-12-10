CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  username VARCHAR(100) NOT NULL UNIQUE,
  email VARCHAR(200) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  token VARCHAR(50) NOT NULL,
  is_teacher BOOLEAN DEFAULT FALSE,
  PRIMARY KEY (id, username, email, token)
);

INSERT INTO users (name, username, email, password)
VALUE  ('John Doe', 'johndoe', 'johndoe@example.com', '123123');


ALTER TABLE users ADD COLUMN profile_image VARCHAR(255) 
DEFAULT '/assets/images/default.jpg';

UPDATE users SET
is_teacher = FALSE
WHERE id = 12;