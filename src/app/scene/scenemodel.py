from PyQt5.QtCore import Qt, QRectF, QLineF, QPointF, QEvent, pyqtSlot
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem, QGraphicsPixmapItem
from PyQt5.QtGui import QPainter, QPen, QColor, QMouseEvent
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

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        if self._currentTool:
            self._currentTool.onMouseMove(e)

        # forward the event to the items in the scene
        if not e.isAccepted():
            super().mouseMoveEvent(e)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        if self._currentTool:
            self._currentTool.onMousePress(e)

        # forward the event to the items in the scene
        if not e.isAccepted():
            super().mousePressEvent(e)

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        if self._currentTool:
            self._currentTool.onMouseRelease(e)

        # forward the event to the items in the scene
        if not e.isAccepted():
            super().mouseReleaseEvent(e)

    @pyqtSlot(str)
    def setTool(self, tool: str) -> None:
        if self._currentTool:
            self._currentTool.disable()
            # let python destroy the current instance
            self._currentTool = None

        try:
            Tool = getattr(imodule(f"app.tool.{tool}".lower()), tool)
            self._currentTool = Tool(scene=self)
            self._currentTool.enable()
        except AttributeError as e:
            print(f"Tool class file not found: {e}")

    @pyqtSlot(bool)
    def setItemsInteractivity(self, val: bool = False):
        for item in self.items():
            if isinstance(item, QGraphicsPixmapItem):
                """The background is always static"""
                continue

            item.setFlag(QGraphicsItem.ItemIsMovable, val)
            item.setFlag(QGraphicsItem.ItemIsSelectable, val)

    # def drawForeground(self, painter: QPainter, rect: QRectF) -> None:
    #     super().drawForeground(painter, rect)

    #     left = int(rect.left())
    #     right = int(rect.right())
    #     top = int(rect.top())
    #     bottom = int(rect.bottom())

    #     first_l = left - (left % kFineGridSize)
    #     first_t = top - (top % kFineGridSize)

    #     grid = []
    #     fine = []

    #     for x in range(first_l, right, kFineGridSize):
    #         if x % kGridSize != 0:
    #             fine.append(QLineF(x, top, x, bottom))
    #         else:
    #             grid.append(QLineF(x, top, x, bottom))

    #     for y in range(first_t, bottom, kFineGridSize):
    #         if y % kGridSize != 0:
    #             fine.append(QLineF(left, y, right, y))
    #         else:
    #             grid.append(QLineF(left, y, right, y))

    #     if len(fine) > 0:
    #         pen = QPen(QColor("#292929"), 1, Qt.DotLine)
    #         pen.setCosmetic(True)
    #         painter.setPen(pen)
    #         painter.drawLines(*fine)

    #     if len(grid) > 0:
    #         pen = QPen(QColor("#2f2f2f"), 1, Qt.SolidLine)
    #         pen.setCosmetic(True)
    #         painter.setPen(pen)
    #         painter.drawLines(*grid)
