from PyQt5.QtCore import Qt, QPointF, QRectF, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (
    QGraphicsScene,
    QGraphicsItem,
    QGraphicsLineItem,
    QGraphicsSceneMouseEvent,
    QWidget,
)
from PyQt5.QtGui import QCursor, QPen, QPainter
from app.object.rectangle import Rectangle
from app.utils.cursordecorators import *
from .abstracttool import AbstractTool, AbstractToolState


class CrossHair(QGraphicsItem):
    def __init__(self, scene: QGraphicsScene = None, parent: QWidget = None):
        super().__init__(parent)

        self.setFlag(QGraphicsItem.ItemIsSelectable, False)

        self._r = scene.views()[0].background.boundingRect()
        self._pos = QPointF(0, 0)

    def setPos(self, point: QPointF) -> None:
        self._pos.setX(point.x())
        self._pos.setY(point.y())

        # Do not call the superclass method to avoid moving the origin coordinate
        # implicitly call update trigger a paint event
        self.update()

    def boundingRect(self) -> QRectF:
        return self._r

    def paint(
        self,
        painter: QPainter,
        option,
        widget: QWidget = None,
    ) -> None:

        pen = QPen(Qt.white, 0, Qt.DashLine)
        painter.setPen(pen)

        painter.drawLine(self._r.left(), self._pos.y(), self._r.right(), self._pos.y())
        painter.drawLine(self._pos.x(), self._r.top(), self._pos.x(), self._r.bottom())


class CaptureRectOrigin(AbstractToolState):
    def mouseMove(self, e: QGraphicsSceneMouseEvent) -> None:
        pass

    def mousePress(self, e: QGraphicsSceneMouseEvent) -> None:
        self.tool._origin = e.scenePos()
        self.tool.createRect(e.scenePos())
        self.tool.transition(DrawRect())

    def mouseRelease(self, e: QGraphicsSceneMouseEvent) -> None:
        pass


class DrawRect(AbstractToolState):
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

        self.tool.transition(CaptureRectOrigin())


class DrawBoxTool(AbstractTool):
    def __init__(self, scene: QGraphicsScene = None):
        super().__init__(scene=scene)

        self._origin: QPointF = None
        self._crossHair = CrossHair(scene=scene)
        self._scene.addItem(self._crossHair)

    def createRect(self, point: QPointF) -> None:
        self._item = Rectangle(position=point, rect=QRectF(0, 0, 0, 0))
        self._scene.addItem(self._item)

    def enable(self) -> None:
        self.transition(CaptureRectOrigin())

    def disable(self) -> None:
        super().disable()
        self._scene.removeItem(self._crossHair)

    def onMouseMove(self, e: QGraphicsSceneMouseEvent) -> None:
        self._crossHair.setPos(e.scenePos())
        self._state.mouseMove(e)

    def onMousePress(self, e: QGraphicsSceneMouseEvent) -> None:
        self._state.mousePress(e)

    def onMouseRelease(self, e: QGraphicsSceneMouseEvent) -> None:
        self._state.mouseRelease(e)

    def onMouseDoubleClick(self, e: QGraphicsSceneMouseEvent) -> None:
        pass
