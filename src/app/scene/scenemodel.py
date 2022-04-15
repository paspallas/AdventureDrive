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
from importlib import import_module as imodule
from typing import Any
from ..tool.abstracttool import AbstractTool
from ..object.background import Grid
from ..model.document import DocumentModel


class SceneModel(QGraphicsScene):
    def __init__(self, document, parent=None):
        super().__init__(parent)

        # The scene document model
        self.document: DocumentModel = document

        self._focusedItem: QGraphicsItem = None
        self._currentTool: AbstractTool = None
        self._editableAreaRect: QRectF = None

        self._setupUi()

    def _setupUi(self):
        self.setBackgroundBrush(QColor("#362F4F"))

    def mouseMoveEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        if self._editableAreaRect.contains(e.scenePos()):
            super().mouseMoveEvent(e)
            if self._currentTool is not None:
                self._currentTool.onMouseMove(e)

    def mousePressEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        if self._editableAreaRect.contains(e.scenePos()):
            super().mousePressEvent(e)
            if self._currentTool is not None:
                self._currentTool.onMousePress(e)

    def mouseReleaseEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        super().mouseReleaseEvent(e)
        if self._currentTool is not None:
            self._currentTool.onMouseRelease(e)

    def mouseDoubleClickEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        super().mouseDoubleClickEvent(e)

        """ Center the double clicked item in the view.
            If no item was selected, zoom out to fit the entire scene
            in the viewport.
        """

        view: QGraphicsView = self.views()[0]
        item: QGraphicsItem = self.itemAt(
            e.scenePos().x(), e.scenePos().y(), view.transform()
        )

        if item is not None:
            if self._focusedItem != item:
                self._focusedItem = item
                self._smoothFocusOnItem(item, view)

    def _smoothFocusOnItem(self, item: QGraphicsItem, view: QGraphicsView) -> None:
        self.animator = QVariantAnimation()
        self.animator.setDuration(800)
        self.animator.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animator.setStartValue(
            view.mapToScene(view.viewport().rect()).boundingRect()
        )

        self.animator.setEndValue(self.getFocusedItemRect())
        self.animator.valueChanged.connect(
            lambda x: view.fitInView(x, Qt.KeepAspectRatio)
        )
        self.animator.start()

    def getFocusedItemRect(self) -> Any:
        item = self._focusedItem
        rect: QRectF = None
        offset = 15

        if item is not None:
            if isinstance(item, Grid):
                rect = item.boundingRect()
            else:
                rect = item.boundingRect().adjusted(-offset, -offset, offset, offset)
            return item.mapRectToScene(rect)
        return None

    def setFocusedItem(self, item: QGraphicsItem) -> None:
        self._focusedItem = item

    def setEditableAreaRect(self, rect: QRectF) -> None:
        self._editableAreaRect = rect

    @pyqtSlot(str)
    def setTool(self, tool: str, checked: bool) -> None:
        # Disable current tool
        if self._currentTool is not None and not checked:
            self._currentTool.disable()
            self._currentTool = None
            return

        # Change current tool
        if self._currentTool is not None and checked:
            self._currentTool.disable()
            self._currentTool = None

        try:
            Tool = getattr(imodule(f"app.tool.{tool}".lower()), tool)
            self._currentTool = Tool(scene=self)
            self._currentTool.enable()
        except AttributeError as e:
            print(f"class attribute not found: {e}")
