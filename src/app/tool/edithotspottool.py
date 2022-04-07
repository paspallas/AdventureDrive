from PyQt5.QtCore import QPointF, QRectF, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem, QGraphicsSceneMouseEvent
from app.object.rectangle import Rectangle
from app.object.editgizmo import EditGizmo
from .abstracttool import AbstractTool, AbstractToolState
from app.utils.cursordecorators import setCursor


class HandleResizerInteraction(AbstractToolState):
    def mouseMove(self, e: QGraphicsSceneMouseEvent) -> None:
        self.tool._item.onMouseMoveEvent(e)

    def mousePress(self, e: QGraphicsSceneMouseEvent) -> None:
        gizmo = self.tool._scene.itemAt(
            e.scenePos(), self.tool._scene.views()[0].transform()
        )
        if gizmo is self.tool._item:
            self.tool._item.onMousePressEvent(e)

    def mouseRelease(self, e: QGraphicsSceneMouseEvent) -> None:
        self.tool._item.onMouseReleaseEvent(e)


class SelectEditableObject(AbstractToolState):
    def mouseMove(self, e: QGraphicsSceneMouseEvent) -> None:
        pass

    def mousePress(self, e: QGraphicsSceneMouseEvent) -> None:
        selected = self.tool._scene.itemAt(
            e.scenePos(), self.tool._scene.views()[0].transform()
        )

        if isinstance(selected, Rectangle):
            self.tool._item = EditGizmo(resizable=selected)
            self.tool._item.setSelected(True)
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

    def onMousePress(self, e: QGraphicsSceneMouseEvent) -> None:
        self._state.mousePress(e)

    def onMouseRelease(self, e: QGraphicsSceneMouseEvent) -> None:
        self._state.mouseRelease(e)

    def onMouseDoubleClick(self, e: QGraphicsSceneMouseEvent) -> None:
        pass
