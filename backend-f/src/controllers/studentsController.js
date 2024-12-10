import connect from '../config/db.js';

export async function academicStageAndLevel(req, res) {
  const grade = req.query.grade;
  const level = req.query.level;
  const id_user = req.query.id;

  if (!grade || !level || !id_user) {
    return res.status(400).json({ error: 'Please fill all fields' });
  }

  try {
    const checkUserSql = "SELECT id FROM users WHERE id = ?;";
    const [userRows] = await connect.execute(checkUserSql, [id_user]);

    if (userRows.length === 0) {
      return res.status(400).json({ error: 'User not found' });
    }
    const checkStudentSql = "SELECT user_id FROM students WHERE user_id = ?;";
    const [studentRows] = await connect.execute(checkStudentSql, [id_user]);
    if (studentRows.length > 0) {
      return res.status(400).json({ error: 'Student data already exists' });
    }
    const insertStudentSql = "INSERT INTO students(user_id, grade, level) VALUES(?, ?, ?);";
    await connect.execute(insertStudentSql, [id_user, grade, level]);
    res.status(200).json({ message: "Student data inserted successfully" });
  } catch (error) {
    console.error("Error inserting user:", error);
    res.status(500).json({ error: 'Error inserting data into the database' });
  }
}

export async function academicStageAndLevelUpdate(req, res) {
  const grade = req.query.grade;
  const level = req.query.level;
  const id_user = req.query.id;

  if (!grade || !level || !id_user) {
    return res.status(400).json({ error: 'Please fill all fields' });
  }

  try {
    
    const checkUserSql = "SELECT id FROM users WHERE id = ?;";
    const [userRows] = await connect.execute(checkUserSql, [id_user]);
    if (userRows.length === 0) {
      return res.status(400).json({ error: 'User not found' });
    }
    const checkStudentSql = "SELECT user_id FROM students WHERE user_id = ?";
    const [studentRows] = await connect.execute(checkStudentSql, [id_user]);
    if (studentRows.length === 0) {
      return res.status(400).json({ error: 'Student data not found' });
    }
    const updateStudentSql = "UPDATE students SET grade = ?, level = ? WHERE user_id = ?;";
    await connect.execute(updateStudentSql, [grade, level, id_user]);
    res.status(200).json({ message: "Student data updated successfully" });
  } catch (error) {
    console.error("Error updating user:", error);
    res.status(500).json({ error: 'Error updating data in the database' });
  }
}