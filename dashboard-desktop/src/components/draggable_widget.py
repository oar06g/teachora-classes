import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint

class DraggableWidget(QWidget):
    def __init__(self):
        super().__init__()

        # إعداد التخطيط والعناصر الداخلية
        self.setWindowTitle("Draggable Widget")
        self.setGeometry(100, 100, 300, 200)

        # إعداد عناصر داخل الودجت
        self.label = QLabel("Drag Me!", self)
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # المتغيرات الخاصة بالسحب
        self.dragging = False
        self.drag_position = QPoint()

    def mousePressEvent(self, event):
        """يتم استدعاؤه عند الضغط على الماوس"""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """يتم استدعاؤه عند تحريك الماوس"""
        if self.dragging:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        """يتم استدعاؤه عند إفلات زر الماوس"""
        self.dragging = False
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # إنشاء النافذة القابلة للسحب
    window = DraggableWidget()
    window.show()

    sys.exit(app.exec_())
