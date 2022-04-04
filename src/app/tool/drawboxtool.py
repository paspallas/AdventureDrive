from PyQt5.QtCore import QPointF, QRectF, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem
from PyQt5.QtGui import QMouseEvent
from app.object.rectangle import Rectangle
from .abstracttool import AbstractTool, AbstractToolState


class ShowHintRectangle(AbstractToolState):
    def mouseMove(self, e: QMouseEvent) -> None:
        self.tool._item.setPos(e.scenePos())

    def mousePress(self, e: QMouseEvent) -> None:
        self.tool._origin = e.scenePos()
        self.tool.transition(PerformDraw())

    def mouseRelease(self, e: QMouseEvent) -> None:
        pass


class PerformDraw(AbstractToolState):
    def mouseMove(self, e: QMouseEvent) -> None:
        sizex, sizey = (
            e.scenePos().x() - self.tool._origin.x(),
            e.scenePos().y() - self.tool._origin.y(),
        )
        sizex, sizey = (sizex if sizex > 0 else 1, sizey if sizey > 0 else 1)
        self.tool._item.setRect(QRectF(0, 0, sizex, sizey))

    def mousePress(self, e: QMouseEvent) -> None:
        pass

    def mouseRelease(self, e: QMouseEvent) -> None:
        self.tool._item.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.tool._item = None
        self.tool._origin = None

        self.tool.transition(ShowHintRectangle())
        self.tool.createHintRect()


class DrawBoxTool(AbstractTool):
    def __init__(self, scene: QGraphicsScene = None):
        super().__init__(scene=scene)

        self._origin: QPointF = None

    def createHintRect(self):
        hintsize = 16
        self._item = Rectangle(
            position=QPointF(0, 0), rect=QRectF(0, 0, hintsize, hintsize)
        )
        self._scene.addItem(self._item)

    def enable(self):
        self.transition(ShowHintRectangle())
        self.createHintRect()

    def disable(self):
        super().disable()

    def onMouseMove(self, e: QMouseEvent) -> None:
        self._state.mouseMove(e)
        e.accept()

    def onMousePress(self, e: QMouseEvent) -> None:
        self._state.mousePress(e)
        e.accept()

    def onMouseRelease(self, e: QMouseEvent) -> None:
        self._state.mouseRelease(e)
        e.accept()

    def onMouseDoubleClick(self, e: QMouseEvent):
        e.accept()
