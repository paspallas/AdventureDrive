from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QStyleFactory
from PyQt5.QtGui import QIcon
from app.ui.mainwindow import MainWindow
from app.utils.settings import SettingsManager
import sys

try:
    from PyQt5.QtWinExtras import QtWin

    QtWin.setCurrentProcessExplicitAppUserModelID("com.paspallas.addrive")
except ImportError:
    pass


def start():
    QApplication.setStyle(QStyleFactory.create("Fusion"))
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    SettingsManager("addrive.ini")

    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
