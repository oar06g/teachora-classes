import aiohttp
import asyncio

BASE_URL = "http://localhost:8000"
CHECK_ADMIN = "/api/dashboard/checkadmin"
GET_COUNT_TEACHERS = "/api/dashboard/getTeacherCount"

class Server:
  def __init__(self): pass

  async def get_count(self, url: str):
    async with aiohttp.ClientSession() as session:  # إنشاء جلسة لجعل الطلبات
      async with session.get(url) as response:  # جعل طلب GET بشكل غير متزامن
        if response.status == 200:  # التحقق مما إذا كان الطلب ناجحًا
          data = await response.json()  # تحليل الاستجابة كـ JSON
          return data.get('count', 0)  # إرجاع عدد المدرسين، افتراضيًا 0 إذا لم يُوجد
        else:
          print(f"خطأ: {response.status}")  # طباعة حالة الخطأ
          return None  # إرجاع None عند الطلبات غير الناجحة

# # مثال على الاستخدام
# async def main():
#   server = Server()
#   url = BASE_URL+GET_COUNT_TEACHERS  # عنوان واجهة برمجة التطبيقات الخاصة بك
#   teacher_count = await server.get_teacher_count(url)  # الحصول على عدد المدرسين
#   print(f'عدد المدرسين: {teacher_count}')  # طباعة عدد المدرسين

# # تشغيل الدالة الرئيسية
# if __name__ == '__main__':
#     asyncio.run(main())
