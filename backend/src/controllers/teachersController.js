import connect from "../config/db.js";

export async function addTeacher(req, res) {
  const id_user = req.query.id;
  const material = req.query.material;

  if (!id || !material) {
    return res.status(400).json({ error: "Please fill all fields" });
  }
  try {
    const checkUserSql = "SELECT id FROM users WHERE id = ?;";
    const [userRows] = await connect.execute(checkUserSql, [id_user]);
    if (userRows.length === 0) {
      return res.status(400).json({ error: "User not found" });
    }
    const checkTeacherSql = "SELECT user_id FROM teachers WHERE user_id = ?;";
    const [teacherRows] = await connect.execute(checkTeacherSql, [id_user]);
    if (teacherRows.length > 0) {
      return res.status(400).json({ error: "Teacher already exists" });
    }
    const updateIsTeacherSql = "UPDATE users SET is_teacher = TRUE WHERE id = ?";
    await connect.execute(updateIsTeacherSql, [id_user]);

    const insertDataSql = "INSERT INTO teachers(user_id, material, is_active) VALUES (?, ?, ?)";
    await connect.execute(insertDataSql, [id_user, material, false]);
    res.status(200).json({ message: "Teacher data inserted successfully" });
  } catch (error) {
    console.log(`Error inserting user: ${error}`);
    res.status(500).json({ error: "Error inserting data into the database" });
  }
}
