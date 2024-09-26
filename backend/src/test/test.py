import requests

BASE_URL = "http://localhost:8000/api/"

def test_add_user():
  data = {
    "name": "Omard",
    "username": "Omard",
    "email": "omard@outlook.com",
    "password": "123123"
  }
  response = requests.post(BASE_URL+"adduser", json=data)
  print(response.text)

def test_check_user():
  data = {
    "email": "test@example.com",
    "password": "password123"
  }
  response = requests.post(BASE_URL+"checkuser", json=data)
  print(response.text)

# test_add_user()
test_check_user()