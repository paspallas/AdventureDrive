from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem, QGraphicsSceneMouseEvent
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
        super().disable()
        self._scene.setItemsInteractivity(False)

    def onMouseMove(self, e: QGraphicsSceneMouseEvent):
        """The selected item handles the event itself"""
        pass

    def onMousePress(self, e: QGraphicsSceneMouseEvent):
        pass

    def onMouseDoubleClick(self, e: QGraphicsSceneMouseEvent):
        pass

    def onMouseRelease(self, e: QGraphicsSceneMouseEvent):
        pass
