from PyQt5.QtCore import QSettings, QPoint, QSize
from PyQt5.QtWidgets import QWidget, QMdiArea
from .singleton import Singleton


class SettingsManager(metaclass=Singleton):
    def __init__(self, configFile: str = None):
        self._configFile = configFile or "app.ini"

    def read(self, widget: QWidget) -> None:
        settings = QSettings(self._configFile, QSettings.IniFormat)
        pos = settings.value("position", QPoint(300, 300))
        size = settings.value("size", QSize(800, 600))
        widget.move(pos)
        widget.resize(size)

    def write(self, widget: QWidget) -> None:
        settings = QSettings(self._configFile, QSettings.IniFormat)
        settings.setValue("position", widget.pos())
        settings.setValue("size", widget.size())
