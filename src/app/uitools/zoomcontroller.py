from PyQt5.QtCore import Qt, QObject, QPoint, QEvent
from PyQt5.QtWidgets import QGraphicsView, QStyleOptionGraphicsItem
from PyQt5.QtGui import QMouseEvent


class ZoomController(QObject):
    """
    This utility class adds zoom control with the mouse wheel to any QGraphicsView object.

    Args:
        widget (QGraphicsView): The graphicsview we want to control.

    """

    zoomFactor = 1.2
    zoomMax = 40
    zoomMin = 0.75

    def __init__(self, widget: QGraphicsView = None):
        super().__init__(widget)

        widget.viewport().installEventFilter(self)

    def eventFilter(self, obj: QObject, e: QEvent) -> bool:
        view: QGraphicsView = obj.parent()

        if view is None:
            return super().eventFilter(obj, e)

        if e.type() == QEvent.Wheel:
            if e.modifiers() & Qt.Modifier.CTRL:
                lod = QStyleOptionGraphicsItem.levelOfDetailFromTransform(
                    view.transform()
                )

                if e.angleDelta().y() > 0:
                    if lod * self.zoomFactor < self.zoomMax:
                        view.scale(self.zoomFactor, self.zoomFactor)
                    else:
                        factorAllowed = self.zoomMax / lod
                        view.scale(factorAllowed, factorAllowed)

                elif e.angleDelta().y() < 0:
                    if lod * (1 / self.zoomFactor) > self.zoomMin:
                        view.scale(1 / self.zoomFactor, 1 / self.zoomFactor)
                    else:
                        factorAllowed = self.zoomMin / lod
                        view.scale(factorAllowed, factorAllowed)

                return True

        return super().eventFilter(obj, e)
