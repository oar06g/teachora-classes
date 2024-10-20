CREATE TABLE IF NOT EXISTS courses (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description VARCHAR(600) NOT NULL,
  teacher_id INT NOT NULL,
  price INT NOT NULL,
  material VARCHAR(255),
  FOREIGN KEY (teacher_id) REFERENCES teachers(id)
);
