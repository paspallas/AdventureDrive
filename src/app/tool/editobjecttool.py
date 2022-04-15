from PyQt5.QtCore import QPointF, QRectF, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (
    QGraphicsScene,
    QGraphicsItem,
    QGraphicsPixmapItem,
    QGraphicsSceneMouseEvent,
)
from app.object.rectangle import Rectangle
from app.object.editgizmo import EditGizmo
from .abstracttool import AbstractTool


class EditObjectTool(AbstractTool):
    def __init__(self, scene: QGraphicsScene = None):
        super().__init__(scene=scene)

    def enable(self) -> None:
        pass

    def disable(self) -> None:
        super().disable()

    def onMouseMove(self, e: QGraphicsSceneMouseEvent) -> None:
        pass

    def onMousePress(self, e: QGraphicsSceneMouseEvent) -> None:
        # Get top most item at mouse click position
        selected = self._scene.itemAt(e.scenePos(), self._scene.views()[0].transform())

        # Never select the background image
        if selected is None or isinstance(selected, QGraphicsPixmapItem):
            if self._item is not None:
                self._scene.removeItem(self._item)
                self._item = None

        elif isinstance(selected, Rectangle):
            if self._item is None:

                # No previous rectangle being edited

                self._item = EditGizmo(editable=selected)
                self._item.setSelected(True)
                self._scene.addItem(self._item)

            else:

                # Edit another rectangle

                self._scene.removeItem(self._item)
                self._item = None
                self._item = EditGizmo(editable=selected)
                self._item.setSelected(True)
                self._scene.addItem(self._item)

    def onMouseRelease(self, e: QGraphicsSceneMouseEvent) -> None:
        pass

    def onMouseDoubleClick(self, e: QGraphicsSceneMouseEvent) -> None:
        pass
