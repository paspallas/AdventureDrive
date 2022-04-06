from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
import decorator
import functools

""" This module provides decorators for changing the current cursor"""


def crossHairCursor(func):
    @functools.wraps(func)
    def setCursor(*args, **kwargs):
        QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
        func(*args, **kwargs)

    return setCursor


def defaultCursor(func):
    @functools.wraps(func)
    def setCursor(*args, **kwargs):
        QApplication.restoreOverrideCursor()
        func(*args, **kwargs)

    return setCursor


def setCursor(klass):
    class DecoratedTool:
        def __init__(self, *args, **kwargs):
            self.tool = klass(*args, **kwargs)

        def __getattr__(self, name):
            method = self.tool.__getattribute__(name)

            if method.__name__ == "enable":
                QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
                return method
            elif method.__name__ == "disable":
                QApplication.restoreOverrideCursor()
                return method
            return method

    return DecoratedTool
