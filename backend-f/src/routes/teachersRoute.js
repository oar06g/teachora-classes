import express from "express";
import {addTeacher} from "../controllers/teachersController.js";

const router = express.Router();

router.post("/adtchr", addTeacher); // addTeacher

export default router;