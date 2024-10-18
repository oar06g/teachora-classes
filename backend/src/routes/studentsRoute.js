import express from "express";
import {academicStageAndLevel} from "../controllers/studentsController.js";

const router = express.Router();

router.post("/academicStageAndLevel", academicStageAndLevel);

export default router;