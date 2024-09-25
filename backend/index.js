import express, { json } from "express";
import * as conf from "./src/config/config.js"
import userRoutes from "./src/routes/userRoute.js";


const app = express();
app.use(express.json())

app.use('/api', userRoutes);

app.listen(conf.port, () => {
  console.log(`listen in http://localhost:${conf.port}`);
})