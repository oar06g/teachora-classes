import express, { json } from "express";
import path from "path";
import { fileURLToPath } from 'url';

import * as conf from "./src/config/config.js"
import userRoutes from "./src/routes/usersRoute.js";
import studentsRoute from "./src/routes/studentsRoute.js";
import teachersRoute from "./src/routes/teachersRoute.js";
import coursesRoute from "./src/routes/coursesRoute.js";


const app = express();
app.use(express.json())
app.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", "*"); // السماح لجميع النطاقات
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  res.header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
  next();
});

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
app.use('/assets', express.static(path.join(__dirname, 'assets')));


app.use('/api', userRoutes);
app.use('/api', studentsRoute);
app.use('/api', teachersRoute);
app.use('/api', coursesRoute);

app.listen(conf.port, () => {
  console.log(`listen in http://localhost:${conf.port}`);
})