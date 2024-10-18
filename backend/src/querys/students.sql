CREATE TABLE IF NOT EXISTS students (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  grade VARCHAR(100) NOT NULL,
  level VARCHAR(100) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO students(user_id, grade, level) VALUES();

DROP TABLE students;