from PyQt5.QtWidgets import (
    QWidget,
    QGraphicsObject,
    QGraphicsItem,
    QGraphicsScene,
)
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from PyQt5.QtCore import Qt, QRectF, QPointF, pyqtSignal, QEvent
from typing import Any
from .rectangle import Rectangle


class Resizer(QGraphicsObject):
    """Resizer handle for object edition"""

    resize = pyqtSignal(QPointF, name="resize")

    def __init__(
        self,
        parent: QWidget = None,
        resizable: Rectangle = None,
    ):
        super().__init__(parent)

        self._rect = QRectF(0, 0, 4, 4)
        self._resizable = resizable

        flags = (
            QGraphicsItem.ItemIsMovable
            | QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemSendsGeometryChanges
        )
        self.setFlags(flags)
        self.setVisible(True)

        position = QPointF(
            self._resizable.scenePos().x() + self._resizable.rect().width(),
            self._resizable.scenePos().y() + self._resizable.rect().height(),
        )
        self.setPos(position)

        # manipulate resizable object
        self.resize.connect(lambda change: self._resizable.resize(change))

    def boundingRect(self) -> QRectF:
        return self._rect

    def paint(
        self,
        painter: QPainter,
        option,
        widget: QWidget = None,
    ) -> None:
        painter.setPen(QPen(Qt.magenta, 1, Qt.SolidLine))
        painter.setBrush(Qt.transparent)
        painter.drawRect(self._rect)

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value: Any) -> Any:
        if change == QGraphicsItem.ItemPositionChange:

            limit = QPointF(
                self._resizable.scenePos().x(), self._resizable.scenePos().y()
            )
            value.setX(value.x() if value.x() >= limit.x() else limit.x())
            value.setY(value.y() if value.y() >= limit.y() else limit.y())

            """ resize by the delta movement"""
            self.resize.emit(value - self.pos())

            return value

        return super().itemChange(change, value)
