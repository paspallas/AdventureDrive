from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QStyleFactory
from PyQt5.QtGui import QIcon, QPixmap
import qtmodern.styles
import qtmodern.windows

from app.ui.mainwindow import MainWindow
from app.utils.settings import SettingsManager
import sys
import logging

try:
    from PyQt5.QtWinExtras import QtWin

    QtWin.setCurrentProcessExplicitAppUserModelID("com.paspallas.addrive")
except ImportError:
    pass


def configureLogging() -> None:
    fmt = "%(levelname)s - %(asctime)s - %(message)s"
    datefmt = "%H:%M:%S"

    logging.basicConfig(
        format=fmt,
        datefmt=datefmt,
        filename="app.log",
        filemode="w",
        level=logging.DEBUG,
    )

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(fmt, datefmt=datefmt))
    logging.getLogger().addHandler(console)


def start() -> None:
    configureLogging()
    logging.getLogger().info("Start application")

    QApplication.setStyle(QStyleFactory.create("Fusion"))
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    SettingsManager("addrive.ini")

    app = QApplication([])
    qtmodern.styles.dark(app)
    window = MainWindow()
    window.show()

    # mw = qtmodern.windows.ModernWindow(window)
    # mw.show()

    sys.exit(app.exec())
