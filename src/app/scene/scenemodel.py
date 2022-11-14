from PyQt5.QtCore import (
    Qt,
    QObject,
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
from PyQt5.QtGui import QPainter, QPen, QColor, QKeyEvent
from typing import Any
from ..object.background import Grid
from ..model.document import DocumentModel


class SceneModel(QGraphicsScene):
    def __init__(self, document: DocumentModel = None, parent: QObject = None):
        super().__init__(parent)

        # The scene document model
        self.document: DocumentModel = document

        self._focusedItem: QGraphicsItem = None
        self._editableAreaRect: QRectF = None

        self.setBackgroundBrush(QColor("#362F4F"))

    def mouseDoubleClickEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        super().mouseDoubleClickEvent(e)

        """ Center the double clicked item in the view.
            If no item was selected, zoom out to fit the entire scene
            in the viewport.
        """

        view = self.views()[0]
        item = self.itemAt(e.scenePos().x(), e.scenePos().y(), view.transform())

        if isinstance(item, Grid):
            return

        if item is not None:
            # Don't focus an already focused item
            if self._focusedItem != item:
                self._focusedItem = item
                self._smoothFocusOnItem(item, view)

    def _smoothFocusOnItem(self, item: QGraphicsItem, view: QGraphicsView) -> None:
        self.animator = QVariantAnimation()
        self.animator.setDuration(800)
        self.animator.setEasingCurve(QEasingCurve.Type.InCurve)
        self.animator.setStartValue(
            # zoom in starting from the current viewport rectangle
            view.mapToScene(view.viewport().rect()).boundingRect()
        )

        self.animator.setEndValue(self.getFocusedItemRect())
        self.animator.valueChanged.connect(
            lambda x: view.fitInView(x, Qt.KeepAspectRatio)
        )
        self.animator.start()

    def _smoothFocusOnSceneRect(self, view: QGraphicsView) -> None:
        self.anim = QVariantAnimation()
        self.anim.setDuration(800)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCurve)
        # zoom out starting from the current focused item
        self.anim.setStartValue(
            self._focusedItem.mapRectToScene(self._focusedItem.boundingRect())
        )
        self.anim.setEndValue(self.sceneRect().adjusted(240, 240, -240, -240))
        self.anim.valueChanged.connect(
            lambda rect: view.fitInView(rect, Qt.KeepAspectRatio)
        )
        self.anim.start()

    def getFocusedItemRect(self) -> Any:
        if self._focusedItem is None:
            return None

        o = 15
        rect = self._focusedItem.boundingRect().adjusted(-o, -o, o, o)
        return self._focusedItem.mapRectToScene(rect)

    def setEditableAreaRect(self, rect: QRectF) -> None:
        self._editableAreaRect = rect

    def keyPressEvent(self, e: QKeyEvent) -> None:
        super().keyPressEvent(e)

        if e.key() == Qt.Key.Key_R:
            if self._focusedItem is not None:
                self._smoothFocusOnSceneRect(self.views()[0])
                self._focusedItem = None
