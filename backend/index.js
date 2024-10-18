import express, { json } from "express";
import * as conf from "./src/config/config.js"
import userRoutes from "./src/routes/userRoute.js";
import studentsRoute from "./src/routes/studentsRoute.js";


const app = express();
app.use(express.json())
app.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", "*"); // السماح لجميع النطاقات
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  res.header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
  next();
});


app.use('/api', userRoutes);
app.use('/api', studentsRoute);

app.listen(conf.port, () => {
  console.log(`listen in http://localhost:${conf.port}`);
})