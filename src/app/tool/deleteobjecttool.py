from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem, QGraphicsSceneMouseEvent
from .abstracttool import AbstractTool
from app.object import *
from app.utils.cursor import setCursor


@setCursor(cursor=":/cursor/eraser")
class DeleteObjectTool(AbstractTool):
    def __init__(self, scene: QGraphicsScene = None):
        super().__init__(scene=scene)

    def enable(self) -> None:
        pass

    def disable(self) -> None:
        super().disable()

    def onMouseMove(self, e: QGraphicsSceneMouseEvent) -> None:
        pass

    def onMousePress(self, e: QGraphicsSceneMouseEvent) -> None:
        object_ = self._scene.itemAt(e.scenePos(), self._scene.views()[0].transform())
        if isinstance(object_, (Rectangle, Sprite)):
            self._scene.removeItem(object_)

    def onMouseRelease(self, e: QGraphicsSceneMouseEvent) -> None:
        pass

    def onMouseDoubleClick(self, e: QGraphicsSceneMouseEvent) -> None:
        pass
