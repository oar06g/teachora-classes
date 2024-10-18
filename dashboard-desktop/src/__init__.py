# ####### DASHBOARD_DESKTOP-PROJECT #########
from PyQt5.QtWidgets import QApplication
import sys
from src.MainWindow import MainWindow

def main():
   app = QApplication(sys.argv)
   window = MainWindow()
   window.show()
   sys.exit(app.exec())
