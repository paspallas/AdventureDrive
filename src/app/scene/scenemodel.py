from PyQt5.QtCore import Qt, QRectF, QLineF, QPointF, QEvent, pyqtSlot
from PyQt5.QtWidgets import (
    QGraphicsScene,
    QGraphicsItem,
    QGraphicsPixmapItem,
    QGraphicsSceneHoverEvent,
    QGraphicsSceneMouseEvent,
)
from PyQt5.QtGui import QPainter, QPen, QColor
from app.tool.abstracttool import AbstractTool
from importlib import import_module as imodule

kGridSize = 128
kFineGridSize = 32


class SceneModel(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._currentTool: AbstractTool = None
        self._setupUi()

    def _setupUi(self):
        self.setBackgroundBrush(QColor("#362F4F"))

    def mouseMoveEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        super().mouseMoveEvent(e)
        if self._currentTool:
            self._currentTool.onMouseMove(e)

    def mousePressEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        super().mousePressEvent(e)
        if self._currentTool:
            self._currentTool.onMousePress(e)

    def mouseReleaseEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        super().mouseReleaseEvent(e)
        if self._currentTool:
            self._currentTool.onMouseRelease(e)

    @pyqtSlot(str)
    def setTool(self, tool: str) -> None:
        if self._currentTool:
            self._currentTool.disable()
            self._currentTool = None

        try:
            Tool = getattr(imodule(f"app.tool.{tool}".lower()), tool)
            self._currentTool = Tool(scene=self)
            self._currentTool.enable()
        except AttributeError as e:
            print(f"Tool class file not found: {e}")

    def drawForeground(self, painter: QPainter, rect: QRectF) -> None:
        super().drawForeground(painter, rect)

        left = int(rect.left())
        right = int(rect.right())
        top = int(rect.top())
        bottom = int(rect.bottom())

        first_l = left - (left % kFineGridSize)
        first_t = top - (top % kFineGridSize)

        grid = []
        fine = []

        for x in range(first_l, right, kFineGridSize):
            if x % kGridSize != 0:
                fine.append(QLineF(x, top, x, bottom))
            else:
                grid.append(QLineF(x, top, x, bottom))

        for y in range(first_t, bottom, kFineGridSize):
            if y % kGridSize != 0:
                fine.append(QLineF(left, y, right, y))
            else:
                grid.append(QLineF(left, y, right, y))

        if len(fine) > 0:
            pen = QPen(QColor("#292929"), 1, Qt.DotLine)
            pen.setCosmetic(True)
            painter.setPen(pen)
            painter.drawLines(*fine)

        if len(grid) > 0:
            pen = QPen(QColor("#2f2f2f"), 1, Qt.SolidLine)
            pen.setCosmetic(True)
            painter.setPen(pen)
            painter.drawLines(*grid)
