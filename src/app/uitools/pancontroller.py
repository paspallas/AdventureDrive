from PyQt5.QtCore import Qt, QObject, QPoint, QEvent
from PyQt5.QtWidgets import QApplication, QAbstractScrollArea
from PyQt5.QtGui import QMouseEvent


class PanController(QObject):
    """
    This utility class adds panning control with the middle mouse button
    to any widget that inherits from QAbstractScrollArea.

    Args:
        widget (QAbstractScrollArea): The widget we want to control.
    """

    def __init__(self, widget: QAbstractScrollArea = None):
        super().__init__(widget)

        widget.viewport().installEventFilter(self)

        self._startPanPoint: QPoint = None

    def eventFilter(self, obj: QObject, e: QEvent) -> bool:

        scrollArea: QAbstractScrollArea = obj.parent()

        if scrollArea is None:
            return super().eventFilter(obj, e)

        if e.type() == QEvent.MouseButtonPress:
            if e.button() == Qt.MidButton:
                # Start panning the view
                QApplication.setOverrideCursor(Qt.OpenHandCursor)

                self._startPanPoint = QPoint(
                    scrollArea.horizontalScrollBar().value() + e.x(),
                    scrollArea.verticalScrollBar().value() + e.y(),
                )

                return True

        elif e.type() == QEvent.MouseMove:
            if (e.buttons() & Qt.MidButton) == Qt.MidButton:
                # Mouse moved while middle mouse button pressed, pan the view

                scrollPoint = QPoint(
                    self._startPanPoint.x() - e.x(),
                    self._startPanPoint.y() - e.y(),
                )

                scrollArea.horizontalScrollBar().setValue(scrollPoint.x())
                scrollArea.verticalScrollBar().setValue(scrollPoint.y())

                return True

        elif e.type() == QEvent.MouseButtonRelease:
            if e.button() == Qt.MidButton:
                QApplication.restoreOverrideCursor()
                QApplication.restoreOverrideCursor()

                return True

        elif e.type() == QEvent.Wheel:
            if e.modifiers() & Qt.Modifier.SHIFT:
                # mouse wheel + shift = scroll the view left - right
                scroll = scrollArea.horizontalScrollBar().value() - e.angleDelta().y()
                scrollArea.horizontalScrollBar().setValue(scroll)

                return True

        return super().eventFilter(obj, e)
