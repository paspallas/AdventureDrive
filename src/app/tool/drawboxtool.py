from PyQt5.QtCore import Qt, QPointF, QRectF, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (
    QGraphicsScene,
    QGraphicsItem,
    QGraphicsLineItem,
    QGraphicsSceneMouseEvent,
)
from PyQt5.QtGui import QCursor, QPen
from app.object.rectangle import Rectangle
from app.utils.cursordecorators import *
from .abstracttool import AbstractTool, AbstractToolState


class ShowHintRectangle(AbstractToolState):
    def mouseMove(self, e: QGraphicsSceneMouseEvent) -> None:
        pass
        # self.tool._item.setPos(e.scenePos())

    def mousePress(self, e: QGraphicsSceneMouseEvent) -> None:
        self.tool._origin = e.scenePos()
        self.tool.transition(PerformDraw())

    def mouseRelease(self, e: QGraphicsSceneMouseEvent) -> None:
        pass


class PerformDraw(AbstractToolState):
    def mouseMove(self, e: QGraphicsSceneMouseEvent) -> None:
        sizex, sizey = (
            e.scenePos().x() - self.tool._origin.x(),
            e.scenePos().y() - self.tool._origin.y(),
        )
        sizex, sizey = (sizex if sizex > 0 else 1, sizey if sizey > 0 else 1)
        self.tool._item.setRect(QRectF(0, 0, sizex, sizey))

    def mousePress(self, e: QGraphicsSceneMouseEvent) -> None:
        pass

    def mouseRelease(self, e: QGraphicsSceneMouseEvent) -> None:
        self.tool._item.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.tool._item = None
        self.tool._origin = None

        self.tool.transition(ShowHintRectangle())
        self.tool.createHintRect()


@setCursor
class DrawBoxTool(AbstractTool):
    def __init__(self, scene: QGraphicsScene = None):
        super().__init__(scene=scene)

        self._origin: QPointF = None
        self._crossh = QGraphicsLineItem(
            self._scene.views()[0].rect().left(),
            0,
            self._scene.views()[0].rect().right(),
            0,
        )
        self._crossv = QGraphicsLineItem(
            0,
            self._scene.views()[0].rect().top(),
            0,
            self._scene.views()[0].rect().bottom(),
        )
        self._crossh.setPen(QPen(Qt.white, 1, Qt.DotLine))
        self._crossv.setPen(QPen(Qt.white, 1, Qt.DotLine))

        self._scene.addItem(self._crossh)
        self._scene.addItem(self._crossv)

    def createHintRect(self) -> None:
        hintsize = 16
        self._item = Rectangle(
            position=QPointF(0, 0), rect=QRectF(0, 0, hintsize, hintsize)
        )
        self._scene.addItem(self._item)

    def enable(self) -> None:
        self.transition(ShowHintRectangle())
        # self.createHintRect()

    def disable(self) -> None:
        super().disable()

    def onMouseMove(self, e: QGraphicsSceneMouseEvent) -> None:
        self._crossh.setPos(self._crossh.pos().x(), e.scenePos().y())
        self._crossv.setPos(e.scenePos().x(), self._crossv.pos().y())
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
