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

data = {
  "id": 12,
  "material": "math"
}

# http://localhost:8000/api/academicStageAndLevel?grade=5&level="secondary"&id=1
# http://localhost:8000/api/adtchr?id=12&material=math

test_obj.test("adtchr", params={"id": 12, "material": "math"})
# test_obj.test('asalu', params={'grade': 2, 'level':'secondary', 'id':1})