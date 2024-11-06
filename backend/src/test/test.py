import requests

class Test:
  def __init__(self, url: str = "http://localhost:8000/api/"):
    self.url = url
  
  def test(self, endpoint: str, method: str = "POST", data: dict = None, params: dict = None):
    def decorator():
      if data:
        response = requests.request(method, self.url + endpoint, json=data)
      elif params:
        response = requests.request(method, self.url + endpoint, params=params)
      print(response.text)
    return decorator()
  
# "https://marten-allowing-camel.ngrok-free.app/api/"
test_obj = Test()

data_user = {
  "name": "test1",
  "username": "test1",
  "email": "test1@test.com",
  "password": "1231231"
}

data_check = {
  "email": "test@test.com",
  "password": "123123"
}

data_course = {
  "title": "كورس لغة عربية",
  "description": "افضل كورس للغة العربية",
  "price": 200,
  "material": "arabic",
  "id": 14,
  "level": "secundry",
  "grade": "one"
}

data_teacher = {
  "id": 14,
  "material": "math"
}


# http://localhost:8000/api/adcourse?title="Math"&description="testing or testing"&price=200&material="math"&id=14
# test_obj.test('adtchr', params=data_teacher)
# test_obj.test('adduser', data=data_user)

# test_obj.test("adcourse", params=data_course)

test_obj.test('getcourse', method="GET", params={
  "level": "ابتدائي",
  "grade": "الصف الأول",
  "material": "العربية"
})