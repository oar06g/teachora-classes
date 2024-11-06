const params = {
  level: "ابتدائي",
  grade: "الصف الأول",
  material: "العربية"
};

const queryString = new URLSearchParams(params).toString();
const url = `https://marten-allowing-camel.ngrok-free.app/api/getcourse?${queryString}`;

fetch(url, {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json'
  }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
