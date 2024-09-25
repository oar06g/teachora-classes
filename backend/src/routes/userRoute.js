import express from 'express';
import { addNewUser, checkUser } from '../controllers/userController.js';

const router = express.Router();

router.post('/adduser', addNewUser);
router.post('/checkuser', checkUser);

export default router;
