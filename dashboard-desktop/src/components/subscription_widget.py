from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QPen, QFont, QColor
import sys

class SubscriptionWidget(QWidget):
    def __init__(self, value=0, max_value=100, parent=None):
        super().__init__(parent)
        self.value = value  # القيمة الحالية
        self.max_value = max_value  # القيمة القصوى
        self.setFixedSize(200, 200)  # حجم الدائرة

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # رسم الدائرة الخلفية
        rect = QRect(10, 10, 180, 180)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(200, 200, 200))
        painter.drawEllipse(rect)

        # رسم الدائرة الأمامية (النسبة)
        painter.setPen(QPen(QColor(0, 150, 255), 10, Qt.SolidLine, Qt.RoundCap))
        angle = int(360 * (self.value / self.max_value))  # حساب الزاوية
        painter.drawArc(rect, -90 * 16, -angle * 16)

        # رسم النص داخل الدائرة (النسبة المئوية)
        painter.setPen(Qt.black)
        painter.setFont(QFont("Arial", 20, QFont.Bold))
        percentage = int((self.value / self.max_value) * 100)
        painter.drawText(rect, Qt.AlignCenter, f"{percentage}%")

    def set_value(self, value):
        self.value = value
        self.update()