import request from 'supertest';
import express from 'express';
import { addNewUser, checkUser } from '../controllers/userController.js'; 
import { describe, it, expect, beforeAll, afterAll } from '@jest/globals';

const app = express();
app.use(express.json());
app.post('/api/adduser', addNewUser);
app.post('/api/checkuser', checkUser);

describe('User API', () => {
  // قبل كل الاختبارات، يمكن إعداد بيانات المستخدم
  beforeAll(async () => {
    // يمكنك إعداد أي بيانات تحتاجها هنا
    await request(app)
      .post('/api/adduser')
      .send({
        name: 'Test User',
        username: 'testuser',
        email: 'test@example.com',
        password: 'password123',
      });
  });

  it('should add a new user successfully', async () => {
    const response = await request(app)
      .post('/api/adduser')
      .send({
        name: 'Another Test User',
        username: 'anothasertestuser',
        email: 'anotheASr@example.com',
        password: 'password123',
      });

    expect(response.status).toBe(201);
    expect(response.body).toHaveProperty('id');
    expect(response.body.name).toBe('Another Test User');
  });

  it('should return error if fields are missing', async () => {
    const response = await request(app)
      .post('/api/adduser')
      .send({
        name: '',
        username: 'testuser',
        email: 'test@example.com',
        password: 'password123',
      });

    expect(response.status).toBe(400);
    expect(response.body.error).toBe('Please fill all fields');
  });

  it('should check if user exists', async () => {
    const response = await request(app)
      .post('/api/checkuser')
      .send({
        email: 'test@example.com',
        password: 'password123',
      });

    expect(response.status).toBe(200);
    expect(response.body).toHaveProperty('username');
  });

  it('should return error if user not found', async () => {
    const response = await request(app)
      .post('/api/checkuser')
      .send({
        email: 'nonexistent@example.com',
        password: 'password123',
      });

    expect(response.status).toBe(404);
    expect(response.body.message).toBe('User not found');
  });

  // بعد انتهاء جميع الاختبارات، يمكنك حذف البيانات الاختبارية إذا كان ذلك ضروريًا
  afterAll(async () => {
    // قم بتنظيف البيانات إذا لزم الأمر
  });
});
