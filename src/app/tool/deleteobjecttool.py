from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem
from PyQt5.QtGui import QMouseEvent
from .abstracttool import AbstractTool


class DeleteObjectTool(AbstractTool):
    def __init__(self, scene: QGraphicsScene = None):
        super().__init__(scene=scene)

    def enable(self) -> None:
        pass

    def disable(self) -> None:
        super().disable()

    def onMouseMove(self, e: QMouseEvent) -> None:
        e.accept()

    def onMousePress(self, e: QMouseEvent) -> None:
        item = self._scene.itemAt(e.scenePos(), self._scene.views()[0].transform())
        if isinstance(item, QGraphicsItem):
            self._scene.removeItem(item)
        e.accept()

    def onMouseRelease(self, e: QMouseEvent) -> None:
        e.accept()

    def onMouseDoubleClick(self, e: QMouseEvent) -> None:
        e.accept()
