import connect from "../config/db.js";

export async function addCourse(req, res) {
  const title = req.query.title;
  const description = req.query.description;
  const price = req.query.price;
  const material = req.query.material;
  const user_id = req.query.id;
  const level = req.query.level;
  const grade = req.query.grade;

  if (!title || !description || !price || !material || !user_id || !level || !grade) {
    return res.status(400).json({ error: 'Please fill all fields' });
  }

  try {
    // =============================
    const checkUserSql = "SELECT id FROM users WHERE id = ?;";
    const [userRows] = await connect.execute(checkUserSql, [user_id]);
    if (userRows.length === 0) {
      return res.status(400).json({ error: 'User not found' });
    }
    // =============================
    const checkTeacherSql = "SELECT is_teacher FROM users WHERE id = ?;";
    const [teacherRows] = await connect.execute(checkTeacherSql, [user_id]);
    if (teacherRows[0].is_teacher === 0) {
      return res.status(400).json({ error: 'User is not a teacher' });
    }
    // =============================
    const checkTeacherIdSql = "SELECT id FROM teachers WHERE user_id = ?;";
    const [teacherCheckRows] = await connect.execute(checkTeacherIdSql, [user_id]);
    if (teacherCheckRows.length === 0) {
      return res.status(400).json({ error: 'Teacher not found' });
    }
    console.log(teacherCheckRows);
    // =============================
    const courseSql = "INSERT INTO courses (title, description, price, material, level, grade, teacher_id) VALUES (?, ?, ?, ?, ?, ?, ?);";
    await connect.execute(courseSql, [title, description, price, material, level, grade, teacherCheckRows[0].id]);

    return res.status(201).json({ message: 'Course added successfully' });
  } catch (error) {
    console.error(error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}

export async function getCourses(req, res) {
  const grade = req.query.grade;
  const level = req.query.level;
  const material = req.query.material;

  if (!grade || !level || !material) {
    return res.status(400).json({ error: "Please fill all fields" });
  }
  
  try {
    const getAllCoursesByMaterialSql = `
      SELECT * FROM courses 
      WHERE grade = ? AND level = ? AND material = ?`;
    
    
    const [courses] = await connect.execute(getAllCoursesByMaterialSql, [grade, level, material]);

    if (courses.length === 0) {
      return res.status(404).json({ message: "No courses found" });
    }

    res.status(200).json({ courses });
  } catch (error) {
    console.error("Error getting courses:", error);
    res.status(500).json({ error: "Error retrieving data from the database" });
  }
}
