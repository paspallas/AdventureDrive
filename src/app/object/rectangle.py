from PyQt5.QtWidgets import (
    QWidget,
    QGraphicsRectItem,
    QGraphicsItem,
    QGraphicsSceneMouseEvent,
)
from PyQt5.QtCore import Qt, QRectF, QPointF, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from typing import Any
from app.utils.serializable import Serializable


class Rectangle(QGraphicsRectItem, Serializable):

    """A rectangle used to delimit areas of interest in the scene"""

    def __init__(
        self,
        position: QPointF,
        rect: QRectF = None,
        parent: QWidget = None,
    ):
        super().__init__(rect, parent=parent)

        self.setPos(position)
        flags = (
            QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemIsFocusable
            | QGraphicsItem.ItemSendsGeometryChanges
            | QGraphicsItem.ItemSendsScenePositionChanges
        )
        self.setFlags(flags)
        self.setAcceptHoverEvents(True)

    def paint(
        self,
        painter: QPainter,
        option,
        widget: QWidget = None,
    ) -> None:

        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(Qt.magenta, 0, Qt.SolidLine)
        brush = QBrush(QColor(Qt.transparent))

        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawRect(self.rect())

        # draw inner shadow
        pen.setColor(QColor(100, 100, 100, 100))
        pen.setWidth(0.6)
        painter.setPen(pen)
        painter.drawRect(self.rect().adjusted(0.5, 0.5, -0.5, -0.5))

    # def itemChange(
    #     self, change: QGraphicsItem.GraphicsItemChange, value: Any
    # ) -> QPointF:
    #     # if change == QGraphicsItem.ItemPositionChange:
    #     """Snap movement to the grid"""
    #     # x = round(value.x() / 32) * 32
    #     # y = round(value.y() / 32) * 32
    #     # return QPointF(x, y)
    #     # return value

    #     return super().itemChange(change, value)

    def mouseMoveEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        if e.buttons() & Qt.LeftButton:
            super().mouseMoveEvent(e)

    @pyqtSlot(QRectF)
    def resize(self, change: QRectF) -> None:
        # """Snap movement to the grid"""
        # x = round(change.x() / 32) * 32
        # y = round(change.y() / 32) * 32

        self.prepareGeometryChange()
        self.setRect(change)

    @pyqtSlot(QPointF)
    def position(self, change: QPointF) -> None:
        self.prepareGeometryChange()
        self.setRect(
            self.rect().adjusted(change.x(), change.y(), change.x(), change.y())
        )

    def serialize(self) -> str:
        return ",".join(
            map(
                lambda item: str(item),
                [
                    self.pos().x(),
                    self.pos().y(),
                    self.rect().width(),
                    self.rect().height(),
                ],
            )
        )

    def deserialize(self, data: str) -> None:
        (i, x, y, w, h) = map(lambda item: float(item), data.split(","))

        # rectangle local coordinates
        self.setRect(self.rect().adjusted(0, 0, w, h))

        # rectangle scene coordinates
        self.setPos(x, y)
