from PyQt5.QtWidgets import QWidget, QGraphicsRectItem, QGraphicsItem, QGraphicsScene
from PyQt5.QtCore import Qt, QRectF, QPointF, pyqtSignal, QEvent, pyqtSlot
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from typing import Any
from .resizer import Resizer
from app.utils.serializable import Serializable


class Rectangle(QGraphicsRectItem, Serializable):

    """This class represents an editable rectangle
    used to delimit areas of interest in the scene
    """

    def __init__(
        self,
        position: QPointF,
        rect: QRectF = None,
        parent: QWidget = None,
        scene: QGraphicsScene = None,
    ):
        super().__init__(rect, parent=parent)
        self._scene = scene

        self.setPos(position)
        flags = (
            QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemIsMovable
            | QGraphicsItem.ItemIsFocusable
            | QGraphicsItem.ItemSendsGeometryChanges
            | QGraphicsItem.ItemSendsScenePositionChanges
        )
        self.setFlags(flags)
        self.setAcceptHoverEvents(True)

        self._resizer = Resizer(parent=self, scene=scene)
        resizerWidth = self._resizer.rect.width() / 2
        resizerOffset = QPointF(resizerWidth, resizerWidth)
        self._resizer.setPos(self.rect().bottomRight() - resizerOffset)

        self._resizer.resized.connect(lambda change: self.resize(change))

    def paint(
        self,
        painter: QPainter,
        option,
        widget: QWidget = None,
    ) -> None:
        pen = QPen(Qt.blue, 3, Qt.SolidLine)
        brush = QBrush(QColor(140, 140, 140, 100))

        if self.isSelected() or self._resizer.isSelected():
            pen.setStyle(Qt.DashLine)
        else:
            brush.setColor(Qt.transparent)

        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawRect(self.rect())

    def itemChange(
        self, change: QGraphicsItem.GraphicsItemChange, value: Any
    ) -> QPointF:
        if change == QGraphicsItem.ItemPositionChange:
            """Snap movement to the grid"""
            # x = round(value.x() / 32) * 32
            # y = round(value.y() / 32) * 32
            # return QPointF(x, y)
            return QPointF(value.x(), value.y())
        else:
            return super().itemChange(change, value)

    def mouseMoveEvent(self, e: QEvent) -> None:
        if e.buttons() & Qt.LeftButton:
            super().mouseMoveEvent(e)
        elif e.buttons() & Qt.RightButton:
            self._resizer.setVisible(True)

    @pyqtSlot(QPointF)
    def resize(self, change: QPointF) -> None:
        # """Snap movement to the grid"""
        # x = round(change.x() / 32) * 32
        # y = round(change.y() / 32) * 32

        self.setRect(self.rect().adjusted(0, 0, change.x(), change.y()).normalized())
        self.prepareGeometryChange()
        self.update()

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
        (i, x, y, w, h) = data.split(",")
        self.setPos(float(x), float(y))
        self.setRect(0, 0, float(w), float(h))
