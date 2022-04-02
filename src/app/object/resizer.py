from PyQt5.QtWidgets import (
    QWidget,
    QGraphicsObject,
    QGraphicsItem,
    QGraphicsScene,
)
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from PyQt5.QtCore import Qt, QRectF, QPointF, pyqtSignal, QEvent
from typing import Any


class Resizer(QGraphicsObject):
    """Resizer handle for object size manipulation"""

    resize = pyqtSignal(QPointF, name="resized")

    def __init__(
        self,
        rect=QRectF(0, 0, 10, 10),
        parent: QWidget = None,
        scene: QGraphicsScene = None,
    ):
        super().__init__(parent)

        self._scene = scene
        self._rect = rect

        flags = (
            QGraphicsItem.ItemIsMovable
            | QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemSendsGeometryChanges
        )
        self.setFlags(flags)
        self.setVisible(False)

    @property
    def rect(self) -> QRectF:
        return self._rect

    def boundingRect(self) -> QRectF:
        """Used by QgraphicsScene to handle collision detection"""
        return self._rect

    def paint(
        self,
        painter: QPainter,
        option,
        widget: QWidget = None,
    ) -> None:
        if self.isSelected():
            painter.setPen(QPen(Qt.blue, 3, Qt.SolidLine))
            painter.setBrush(Qt.white)
        painter.drawRect(self._rect)

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value: Any) -> Any:
        if change == QGraphicsItem.ItemPositionChange:
            if self.isSelected():
                self.resize.emit(value - self.pos())
        return value
