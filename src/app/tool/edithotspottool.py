from PyQt5.QtCore import QPointF, QRectF, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem, QGraphicsSceneMouseEvent
from app.object.rectangle import Rectangle
from app.object.resizer import Resizer
from .abstracttool import AbstractTool, AbstractToolState


class HandleResizerInteraction(AbstractToolState):
    def mouseMove(self, e: QGraphicsSceneMouseEvent) -> None:
        # if self.tool._item.isSelected():
        self.tool._item.mouseMoveEvent(e)
        # self.tool._item.setPos(e.scenePos())

    def mousePress(self, e: QGraphicsSceneMouseEvent) -> None:
        # resizer = self.tool._scene.itemAt(
        #     e.scenePos(), self.tool._scene.views()[0].transform()
        # )

        # if resizer is self.tool._item:
        self.tool._item.setSelected(True)
        self.tool._item.mousePressEvent(e)

    def mouseRelease(self, e: QGraphicsSceneMouseEvent) -> None:
        self.tool._item.mouseReleaseEvent(e)
        # if resizer is self.tool._item:
        #     self.tool._item.onMouseRelease(e)
        # self.tool._item.setSelected(False)


class SelectEditableObject(AbstractToolState):
    def mouseMove(self, e: QGraphicsSceneMouseEvent) -> None:
        pass

    def mousePress(self, e: QGraphicsSceneMouseEvent) -> None:
        selected = self.tool._scene.itemAt(
            e.scenePos(), self.tool._scene.views()[0].transform()
        )

        if isinstance(selected, Rectangle):
            self.tool._item = Resizer(resizable=selected)
            self.tool._scene.addItem(self._tool._item)
            self.tool.transition(HandleResizerInteraction())

    def mouseRelease(self, e: QGraphicsSceneMouseEvent) -> None:
        pass


class EditHotSpotTool(AbstractTool):
    def __init__(self, scene: QGraphicsScene = None):
        super().__init__(scene=scene)

    def enable(self) -> None:
        self.transition(SelectEditableObject())

    def disable(self) -> None:
        super().disable()

    def onMouseMove(self, e: QGraphicsSceneMouseEvent) -> None:
        self._state.mouseMove(e)
        e.accept()

    def onMousePress(self, e: QGraphicsSceneMouseEvent) -> None:
        self._state.mousePress(e)
        e.accept()

    def onMouseRelease(self, e: QGraphicsSceneMouseEvent) -> None:
        self._state.mouseRelease(e)
        e.accept()

    def onMouseDoubleClick(self, e: QGraphicsSceneMouseEvent) -> None:
        e.accept()
