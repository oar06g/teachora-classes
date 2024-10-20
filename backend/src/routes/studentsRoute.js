import express from "express";
import {academicStageAndLevel, academicStageAndLevelUpdate} from "../controllers/studentsController.js";

const router = express.Router();

router.post("/asal", academicStageAndLevel); // academicStageAndLevel
router.post("/asalu", academicStageAndLevelUpdate); // academicStageAndLevelUpdate

export default router;