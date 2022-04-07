from PyQt5.QtWidgets import (
    QWidget,
    QGraphicsItem,
    QGraphicsPixmapItem,
    QGraphicsRectItem,
)
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QLineF, QPointF, QRectF, pyqtSlot


class Grid(QGraphicsRectItem):

    FINE_GRID_SIZE = 16

    def __init__(self, position: QPointF, rect: QRectF = None, parent: QWidget = None):
        super().__init__(rect, parent)

        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, False)
        self.setFlag(QGraphicsItem.ItemIsFocusable, False)
        self.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.setFlag(QGraphicsItem.ItemIsMovable, False)

    def paint(
        self,
        painter: QPainter,
        option,
        widget: QWidget = None,
    ) -> None:

        rect = self.boundingRect().toRect()
        left = rect.left()
        right = rect.right()
        top = rect.top()
        bottom = rect.bottom()

        fine = []

        for x in range(0, right, self.FINE_GRID_SIZE):
            fine.append(QLineF(x, top, x, bottom))

        for y in range(0, bottom, self.FINE_GRID_SIZE):
            fine.append(QLineF(left, y, right, y))

        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(QColor("#202020"), 0, Qt.DotLine)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLines(*fine)


class BackGround(QGraphicsPixmapItem):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent=parent)

        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, False)
        self.setFlag(QGraphicsItem.ItemIsFocusable, False)
        self.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.grid: Grid = None

    @pyqtSlot()
    def enableGrid(self) -> None:
        self.grid = Grid(position=self.pos(), rect=self.boundingRect())
        self.scene().addItem(self.grid)

    @pyqtSlot()
    def disableGrid(self) -> None:
        self.scene().removeItem(self.grid)
        self.grid = None
