# API 

##  API Documentation

link server: https://marten-allowing-camel.ngrok-free.app

1. Add new user `/api/adduser` { name, username, email, password }
- `201` Status successful
- `400` Status bad request
- `500` the server encountered an unexpected condition that prevented it from fulfilling the request

2. Check user exist `/api/checkuser` { email, password }
- `404` Not found
- `401` Unauthorized
- `200` the request was successful
- `500` the server encountered an unexpected condition that prevented it from fulfilling the request

3. Add Academic Stage And Level `/asal?grade=5&level="secondary"&id=1` { grade, level, id }
- `400` Bad request
- `500` the server encountered an unexpected condition that prevented it from fulfilling the request
- `200` request Ok

4. Update Academic Stage And Level `/asalu?grade=5&level="secondary"&id=1` { grade, level, id }
- `400` Bad request
- `500` the server encountered an unexpected condition that prevented it from fulfilling the request
- `200` request Ok

5. Add Teacher `/adtchr?id=1&material="math"` { id, material }
- `400` Bad request
- `500` the server encountered an unexpected condition that prevented it from fulfilling the request
- `200` Status Ok

6. Add Courses `/adcourse?title=""&description=""&price=""&material=""&user_id=5` { title, description, price, material, id, level, grade }
- `400` Bad request
- `201` Status successful
- `500` the server encountered an unexpected condition that prevented it from fulfilling the request