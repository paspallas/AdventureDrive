from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem
from PyQt5.QtGui import QMouseEvent
from abc import ABC, abstractmethod


class AbstractTool(ABC):
    def __init__(self, scene: QGraphicsScene = None):
        self._scene: QGraphicsScene = scene
        self._origin: QPointF = None
        self._item: QGraphicsItem = None

        self.enable()

    @classmethod
    @abstractmethod
    def enable(self):
        pass

    @classmethod
    @abstractmethod
    def disable(self):
        pass

    @classmethod
    @abstractmethod
    def onMouseMove(self, e: QMouseEvent):
        pass

    @classmethod
    @abstractmethod
    def onMousePress(self, e: QMouseEvent):
        pass

    @classmethod
    @abstractmethod
    def onMouseDoubleClick(self, e: QMouseEvent):
        pass

    @classmethod
    @abstractmethod
    def onMouseRelease(self, e: QMouseEvent):
        pass
