from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem
from PyQt5.QtGui import QMouseEvent
from .abstracttool import AbstractTool


class SelectTool(AbstractTool):
    def __init__(self, scene: QGraphicsScene = None):
        super().__init__(scene=scene)

    def enable(self):
        pass

    def disable(self):
        for item in self._scene.selectedItems():
            item.setSelected(False)

    def onMouseMove(self, e: QMouseEvent):
        pass

    def onMousePress(self, e: QMouseEvent):
        pass

    def onMouseDoubleClick(self, e: QMouseEvent):
        pass

    def onMouseRelease(self, e: QMouseEvent):
        pass
