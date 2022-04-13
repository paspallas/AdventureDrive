from PyQt5.QtCore import Qt, QPointF, QLineF, QRectF, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (
    QGraphicsScene,
    QGraphicsItem,
    QGraphicsSceneMouseEvent,
    QWidget,
)
from PyQt5.QtGui import QCursor, QPen, QPainter
from ..utils.cursor import setCursor
from .abstracttool import AbstractTool, AbstractToolState

from ..utils.serializable import Serializable


class Polygon(QGraphicsItem, Serializable):
    def __init__(self, parent: QGraphicsItem):
        super().__init__(parent)

        self._points: list[QPointF] = list()

    def addPoint(self, point: QPointF) -> None:
        self._points.append(point)

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, 0, 0)

    def serialize(self) -> str:
        pass

    def deserialize(self) -> None:
        pass


class PolygonTool(AbstractTool):
    def __init__(self, scene: QGraphicsScene = None):
        super().__init__(scene)

    def enable(self):
        pass

    def disable(self):
        super().disable()

    def onMouseMove(self, e: QGraphicsSceneMouseEvent) -> None:
        pass

    def onMousePress(self, e: QGraphicsSceneMouseEvent) -> None:
        pass

    def onMouseRelease(self, e: QGraphicsSceneMouseEvent) -> None:
        pass

    def onMouseDoubleClick(self, e: QGraphicsSceneMouseEvent) -> None:
        pass
