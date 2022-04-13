from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QStatusBar
from threading import Lock, Thread


class Singleton(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance

        return cls._instances[cls]._bar


class StatusBar(metaclass=Singleton):
    def __init__(self):
        self._bar = QStatusBar()
