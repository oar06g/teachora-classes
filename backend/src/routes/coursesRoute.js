import express from "express";
import {addCourse, getCourses} from "../controllers/coursesController.js";

const router = express.Router();

router.post("/adcourse", addCourse);
router.get("/getcourse", getCourses);

export default router;