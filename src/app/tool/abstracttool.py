from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem
from PyQt5.QtGui import QMouseEvent
from abc import ABC, ABCMeta, abstractmethod


class AbstractTool:
    pass


class AbstractToolState(ABC):
    @property
    def tool(self) -> AbstractTool:
        return self._tool

    @tool.setter
    def tool(self, tool: AbstractTool) -> None:
        self._tool = tool

    @classmethod
    @abstractmethod
    def mouseMove(self, e: QMouseEvent) -> None:
        pass

    @classmethod
    @abstractmethod
    def mousePress(self, e: QMouseEvent) -> None:
        pass

    @classmethod
    @abstractmethod
    def mouseRelease(self, e: QMouseEvent) -> None:
        pass


class AbstractObject(ABCMeta, type(QObject)):
    pass


class AbstractTool(ABC, metaclass=AbstractObject):
    def __init__(self, scene: QGraphicsScene = None):

        self._scene: QGraphicsScene = scene
        self._item: QGraphicsItem = None
        self._state: AbstractToolState = None

    def transition(self, state: AbstractToolState):
        self._state = state
        self._state.tool = self

    @classmethod
    @abstractmethod
    def enable(self) -> None:
        pass

    def disable(self) -> None:
        self._state = None

        if self._item:
            self._scene.removeItem(self._item)
            self._item = None

    @classmethod
    @abstractmethod
    def onMouseMove(self, e: QMouseEvent) -> None:
        pass

    @classmethod
    @abstractmethod
    def onMousePress(self, e: QMouseEvent) -> None:
        pass

    @classmethod
    @abstractmethod
    def onMouseDoubleClick(self, e: QMouseEvent) -> None:
        pass

    @classmethod
    @abstractmethod
    def onMouseRelease(self, e: QMouseEvent) -> None:
        pass

    @pyqtSlot(bool)
    def snapToGrid(val: bool) -> None:
        pass
