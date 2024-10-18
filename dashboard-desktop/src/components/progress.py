from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QFont, QColor, QPen
from PyQt5.QtCore import Qt, QRectF


class CircularProgress(QWidget):
    def __init__(self, money, max_money, parent=None):
        super(CircularProgress, self).__init__(parent)
        self.money = money         # الأموال التي لديك
        self.max_money = max_money # الحد الأقصى
        self.percentage = (self.money / self.max_money) * 100

        self.setMinimumSize(100, 100)  # حجم مبدئي

    def paintEvent(self, event):
        # إعداد الرسام (QPainter)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # حجم الدائرة
        rect = QRectF(10, 10, self.width() - 20, self.height() - 20)

        # رسم الخلفية (دائرة خفيفة)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(250, 250, 250))
        painter.drawEllipse(rect)

        # إعداد القلم للرسم
        pen = QPen()
        pen.setWidth(10)
        pen.setColor(QColor(116, 47, 199))  # لون الدائرة
        painter.setPen(pen)

        # رسم الدائرة المتقدمة حسب النسبة المئوية
        angle = int(360 * (self.percentage / 100))
        painter.drawArc(rect, -90 * 16, -angle * 16)

        # كتابة القيمة (عدد الأموال) في المنتصف
        painter.setPen(QPen(Qt.black))
        painter.setFont(QFont('Arial', 20))
        text = f"${int(self.money)}"  # صيغة الأموال
        painter.drawText(rect, Qt.AlignCenter, text)