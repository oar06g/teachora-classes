import asyncio
import aiohttp
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import json

from src.Ui_interface import Ui_dashboard_desktop
from src.components.progress import CircularProgress
from src.components.subscription_widget import SubscriptionWidget
from src.utils.server import Server

BASE_URL = "http://127.0.0.1:8000"
CHECK_ADMIN = "/api/dashboard/checkadmin"
GET_COUNT_TEACHERS = "/api/dashboard/getteachercount"
GET_COUNT_STUDENT = "/api/dashboard/getstudentcount"

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_dashboard_desktop()
        self.ui.setupUi(self)

        with open("./Json/style.json", 'r') as jsons:
            JsonCode = jsons.read()
            load_json = json.loads(JsonCode)

            self.setWindowTitle(str(load_json["TitleApplication"]))

        self.ui.login_btn.clicked.connect(self.Login)

        self.progress = SubscriptionWidget(value=20)  # تحديد النسبة الحالية
        self.ui.verticalLayout_8.addWidget(self.progress)
        
        # self.ui.pushButton_2.clicked.connect(self.update_header_items)
        
        # تحديث عدد المدرسين عند بدء التطبيق
        asyncio.run(self.update_header_items())

    async def update_header_items(self):
        server = Server()
        teacher_count = await server.get_count(BASE_URL+GET_COUNT_TEACHERS)
        student_count = await server.get_count(BASE_URL+GET_COUNT_STUDENT)

        if teacher_count is not None :
            self.ui.number_2.setText(str(teacher_count))
        else:
            self.ui.number_2.setText("Error fetching count")
        if student_count is not None :
            self.ui.number.setText(str(student_count))
        else:
            self.ui.number.setText("Error fetching count")

    def update_money(self, new_money):
        self.progress.money = new_money
        self.progress.percentage = (new_money / self.progress.max_money) * 100
        self.progress.update()
  
    # switch function
    def switch(self, widget_page):
        self.ui.stackedWidget.setCurrentWidget(widget_page)

    async def check_server_work(self, url: str):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=3) as response:  # زيادة المهلة إلى 3 ثوانٍ
                    return 200 <= response.status < 300
            except asyncio.TimeoutError:
                print("Server is not responding: Timeout")
                return False
            except aiohttp.ClientError as e:
                print(f"Client error: {e}")
                return False

    async def check_admin(self, data: dict, url: str):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=data) as response:
                    if response.status == 400:
                        return False
                    elif response.status == 200:
                        return True
                    elif response.status == 404:
                        print("User not found")
                        return False
                    elif response.status == 401:
                        print("Invalid credentials")
                        return False
                    else:
                        print(f"Unexpected status code: {response.status}")
                        return None
            except aiohttp.ClientError as e:
                print(f"Error occurred: {e}")
                return None

    def Login(self):
        self._username = self.ui.username_input.text()
        self._password = self.ui.password_input.text()
        data = {
            "username": self._username,
            "password": self._password
        }

        asyncio.run(self.perform_login(data))

    async def perform_login(self, data: dict):
        server_is_up = await self.check_server_work(BASE_URL)
        if server_is_up:
            check = await self.check_admin(data, url=BASE_URL + CHECK_ADMIN)
            if check:
                self.ui.stackedWidget.setCurrentIndex(1)
            else:
                self.ui.error_label.setText("Username or Password is incorrect")
        else:
            self.ui.error_label.setText("Server is not reachable")
