import connect from "../config/db.js";
import bcrypt from "bcrypt";

export async function addNewUser(req, res) {
  // get data json
  const { name, username, email, password } = req.body;
  try {
    // create password hash
    const hashedPassword = await bcrypt.hash(password, 10);
    const sql = `INSERT INTO users (name, username, email, password) VALUES (?, ?, ?, ?)`;
    const result = await connect.execute(sql, [name, username, email, hashedPassword]);

    res.status(201).json({ id: result.insertId, name, username, email });
  } catch (err) {
      console.error(err);
      res.status(500).json({ error: 'Database insert error' });
  }
}

export async function checkUser(req, res) {
  const { email, password } = req.body;
  const sql = `SELECT * FROM users WHERE email = ?`;

  try {
    const [results] = await connect.execute(sql, [email]);
    if (!results || results.length === 0) {
        return res.status(404).json({ message: 'User not found' });
    }

    const user = results[0];
    
    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) return res.status(401).json({ message: 'Invalid credentials' });

    const { password: _, ...userData } = user;
    res.status(200).json(userData);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Database query error' });
  }
}