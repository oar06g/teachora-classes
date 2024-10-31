CREATE TABLE IF NOT EXISTS courses (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description VARCHAR(600) NOT NULL,
  teacher_id INT NOT NULL,
  price INT NOT NULL,
  material VARCHAR(255),
  grade VARCHAR(100) NOT NULL,
  level VARCHAR(100) NOT NULL,
  FOREIGN KEY (teacher_id) REFERENCES teachers(id)
);

-- secondary
SELECT * FROM courses
WHERE material = "Math"  AND grade = 2 AND level = "sucndry";


ALTER TABLE courses
ADD COLUMN grade VARCHAR(255);

ALTER TABLE courses
ADD COLUMN level VARCHAR(255);

