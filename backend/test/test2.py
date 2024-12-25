import requests
import threading
import random
import string
import json

# إعدادات API
url = "http://127.0.0.1:8000/api/v1/adduser/"  # استبدل هذا بعنوان API الخاص بك
threads = 50  # عدد مؤشرات التنفيذ
requests_count = 10  # عدد الطلبات لكل مؤشر

# توليد بيانات وهمية
def generate_fake_data():
    full_name = ''.join(random.choices(string.ascii_letters, k=10)) + " " + ''.join(random.choices(string.ascii_letters, k=10))
    username = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    gender = random.choice(["male", "female"])
    email = ''.join(random.choices(string.ascii_lowercase, k=8)) + "@example.com"
    is_teacher = random.choice([True, False])

    return {
        "full_name": full_name,
        "username": username,
        "password": password,
        "gender": gender,
        "email": email,
        "is_teacher": is_teacher
    }


# إرسال الطلبات
def send_request():
    for _ in range(requests_count):
        try:
            payload = generate_fake_data()
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, data=json.dumps(payload), headers=headers)
            print(f"Response {response.status_code}: {response.text}")
        except Exception as e:
            print(f"خطأ: {e}")


# تشغيل مؤشرات التنفيذ
threads_list = []
for i in range(threads):
    thread = threading.Thread(target=send_request)
    thread.start()
    threads_list.append(thread)

# الانتظار حتى تنتهي جميع المؤشرات
for thread in threads_list:
    thread.join()

print("الاختبار انتهى!")
