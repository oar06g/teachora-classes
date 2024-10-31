import mysql from "mysql2/promise.js";

const connect = mysql.createPool({
  host: '192.168.1.100',
  user: 'titan',
  password: '++++++',
  database: 'teachoradb'
})

export default connect;