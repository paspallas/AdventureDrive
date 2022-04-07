from PyQt5.QtCore import (
    Qt,
    QRectF,
    QLineF,
    QPointF,
    QEvent,
    QVariantAnimation,
    QEasingCurve,
    pyqtSlot,
)
from PyQt5.QtWidgets import (
    QGraphicsScene,
    QGraphicsView,
    QGraphicsItem,
    QGraphicsPixmapItem,
    QGraphicsSceneHoverEvent,
    QGraphicsSceneMouseEvent,
)
from PyQt5.QtGui import QPainter, QPen, QColor
from app.tool.abstracttool import AbstractTool
from importlib import import_module as imodule


class SceneModel(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.focusedItem: QGraphicsItem = None
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

    def mouseDoubleClickEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        super().mouseDoubleClickEvent(e)

        """ Center the double clicked item in the view"""

        view: QGraphicsView = self.views()[0]
        item: QGraphicsItem = self.itemAt(
            e.scenePos().x(), e.scenePos().y(), view.transform()
        )

        if item is not None:
            if self.focusedItem != item:
                self.focusedItem = item
                self._smoothFocusOnItem(item, view)

    def _smoothFocusOnItem(self, item: QGraphicsItem, view: QGraphicsView) -> None:
        self.animator = QVariantAnimation()
        self.animator.setDuration(800)
        self.animator.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animator.setStartValue(
            view.mapToScene(view.viewport().rect()).boundingRect()
        )
        self.animator.setEndValue(item.mapRectToScene(item.boundingRect()))
        self.animator.valueChanged.connect(
            lambda x: view.fitInView(x, Qt.KeepAspectRatio)
        )
        self.animator.start()

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

        fineGridSize = 16

        left = int(rect.left())
        right = int(rect.right())
        top = int(rect.top())
        bottom = int(rect.bottom())

        first_l = left - (left % fineGridSize)
        first_t = top - (top % fineGridSize)

        fine = []

        for x in range(first_l, right, fineGridSize):
            fine.append(QLineF(x, top, x, bottom))

        for y in range(first_t, bottom, fineGridSize):
            fine.append(QLineF(left, y, right, y))

        pen = QPen(QColor("#292929"), 0, Qt.DotLine)
        painter.setPen(pen)
        painter.drawLines(*fine)
