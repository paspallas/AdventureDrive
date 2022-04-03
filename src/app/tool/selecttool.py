from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem
from PyQt5.QtGui import QMouseEvent
from .abstracttool import AbstractTool


class SelectTool(AbstractTool):
    """This tool acts as a proxy for the native
    QGraphicsScene item selection handling
    """

    def __init__(self, scene: QGraphicsScene = None):
        super().__init__(scene=scene)

    def enable(self):
        self._scene.setItemsInteractivity(True)

    def disable(self):
        self._scene.setItemsInteractivity(False)

    def onMouseMove(self, e: QMouseEvent):
        pass

    def onMousePress(self, e: QMouseEvent):
        pass

    def onMouseDoubleClick(self, e: QMouseEvent):
        pass

    def onMouseRelease(self, e: QMouseEvent):
        pass
