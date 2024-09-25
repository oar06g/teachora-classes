import mysql from "mysql2/promise.js";

const connect = mysql.createPool({
  host: '192.168.1.100',
  user: 'titan',
  password: 'titan123123=+123123',
  database: 'teachoradb'
})

export default connect;