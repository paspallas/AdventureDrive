from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QStatusBar
from app.utils.singleton import Singleton


class StatusBar(metaclass=Singleton):
    def __init__(self):
        self._bar = QStatusBar()

    @property
    def bar(self) -> QStatusBar:
        return self._bar
