import express from "express";
import {addCourse} from "../controllers/coursesController.js";

const router = express.Router();

router.post("/adcourse", addCourse);

export default router;