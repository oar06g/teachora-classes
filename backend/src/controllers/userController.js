import connect from "../config/db.js";
import bcrypt from "bcrypt";

/**
 * Function to generate a random token with a specified length.
 * @param {number} length - The length of the token to generate.
 * @returns {string} - A random token consisting of alphanumeric characters.
 */
function generateTokens(length) {
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let token = '';

  for (let i = 0; i < length; i++) {
    token += characters.charAt(Math.floor(Math.random() * characters.length));
  }

  return token;
}

/**
 * Function to recursively check if a token exists in the database and generate a new one if it does.
 * @returns {string} - A unique token that doesn't exist in the database.
 */
async function checkTokenExist() {
  const randomToken = generateTokens(35);
  const sql = "SELECT * FROM users WHERE token = ?";

  try {
    const [results] = await connect.execute(sql, [randomToken]);

    if (results.length > 0) {
      console.log("Token exists, generating new one...");
      return checkTokenExist(); // Recursively generate a new token
    } else {
      console.log("Token does not exist, returning token.");
      return randomToken;
    }
  } catch (err) {
    console.error("Error while checking token existence:", err.message);
    throw new Error('Database error while checking token');
  }
}

/**
 * Function to add a new user to the database.
 * @param {Object} req - The request object containing user details.
 * @param {Object} res - The response object to send back data.
 * @returns {Promise<void>}
 */
export async function addNewUser(req, res) {
  const { name, username, email, password, is_teacher } = req.body;

  // Ensure all required fields are provided
  if (!name || !username || !email || !password) {
    return res.status(400).json({ error: 'Please fill all fields' });
  }

  try {
    // Generate a unique token for the user
    const token = await checkTokenExist();
    console.log("Generated Token:", token);

    // Hash the user's password before storing it
    const hashedPassword = await bcrypt.hash(password, 10);

    // SQL query to insert user details into the database
    const sql = `INSERT INTO users (name, username, email, password, token, is_teacher) VALUES (?, ?, ?, ?, ?, ?)`;
    const [result] = await connect.execute(sql, [name, username, email, hashedPassword, token, is_teacher]);

    // Respond with success and user data (excluding password)
    res.status(201).json({ id: result.insertId, name, username, email, token, is_teacher });
  } catch (err) {
    if (err.code === 'ER_DUP_ENTRY') {
      return res.status(400).json({ error: 'The username or email already exists' });
    }

    console.error("Error inserting user:", err);
    res.status(500).json({ error: 'Error inserting data into the database' });
  }
}

/**
 * Function to check if a user exists and validate their credentials.
 * @param {Object} req - The request object containing login details.
 * @param {Object} res - The response object to send back data.
 * @returns {Promise<void>}
 */
export async function checkUser(req, res) {
  const { email, password } = req.body;

  // SQL query to find the user by email
  const sql = `SELECT * FROM users WHERE email = ?`;

  try {
    const [results] = await connect.execute(sql, [email]);

    if (!results || results.length === 0) {
      return res.status(404).json({ message: 'User not found' });
    }

    const user = results[0];

    // Compare the provided password with the stored hashed password
    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) {
      return res.status(401).json({ message: 'Invalid credentials' });
    }

    // Omit the password field from the response
    const { password: _, ...userData } = user;
    res.status(200).json(userData);

  } catch (err) {
    console.error("Error during user authentication:", err);
    res.status(500).json({ error: 'Database query error' });
  }
}
