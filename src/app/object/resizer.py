from PyQt5.QtWidgets import QWidget, QGraphicsScene, QGraphicsObject, QGraphicsItem
from PyQt5.QtGui import QPainter, QPainterPath, QPen, QColor, QBrush, QMouseEvent
from PyQt5.QtCore import Qt, QRectF, QSize, QPointF, pyqtSignal, QEvent
from typing import Any, Dict
from .rectangle import Rectangle


class Resizer(QGraphicsObject):
    """Resizer handle for object edition"""

    resize = pyqtSignal(QRectF, name="resize")
    positionChange = pyqtSignal(QPointF, name="positionChange")

    def __init__(
        self,
        parent: QWidget = None,
        resizable: Rectangle = None,
    ):
        super().__init__(parent)

        self._resizable = resizable
        self._rect: QRectF = resizable.rect()

        self._mouseOrigin: QPointF = None
        self._boundingRectPoint: QPointF = None
        self._handleSize = 4
        self._selectedHandle: int = None
        self._handles: Dict[str, QRectF] = {}

        flags = (
            QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemSendsGeometryChanges
            | QGraphicsItem.ItemIsFocusable
        )
        self.setFlags(flags)
        self.setVisible(True)
        self.setAcceptHoverEvents(True)

        """ Place the resizer gizmo over the resizable object"""
        self.setPos(self._resizable.scenePos())
        self._updateHandlePositions()

        """ Manipulate resizable object """
        self.resize.connect(lambda change: self._resizable.resize(change))

    def _handleAt(self, point: QPointF) -> Any:

        """
        Return the handle at the given point.
        All rect coordinates are stored in 'local' space
        """

        for handle, rect in self._handles.items():
            if self.mapRectToScene(rect).contains(point):
                return handle
        return None

    def _updateHandlePositions(self):
        s = self._handleSize
        o = s // 2
        b = self._rect

        """ Center the handles in the corners of the bounding rect """
        self._handles["TopLeft"] = QRectF(b.left() - o, b.top() - o, s, s)
        self._handles["Left"] = QRectF(b.left() - o, b.center().y(), s, s)
        self._handles["BottomLeft"] = QRectF(b.left() - o, b.bottom() - o, s, s)
        self._handles["TopRight"] = QRectF(b.right() - o, b.top() - o, s, s)
        self._handles["Right"] = QRectF(b.right() - o, b.center().y(), s, s)
        self._handles["BottomRight"] = QRectF(b.right() - o, b.bottom() - o, s, s)
        self._handles["Top"] = QRectF(b.center().x(), b.top() - o, s, s)
        self._handles["Bottom"] = QRectF(b.center().x(), b.bottom() - o, s, s)

    def boundingRect(self) -> QRectF:

        """Adjust the bounding rect so that it contains the handles"""

        return self._rect.adjusted(
            -self._handleSize, -self._handleSize, self._handleSize, self._handleSize
        )

    def shape(self) -> QPainterPath:
        path = QPainterPath()
        path.addRect(self._rect)
        if self.isSelected():
            for shape in self._handles.values():
                path.addEllipse(shape)
        return path

    def _performResize(self, currentMouse: QPointF) -> None:

        handle = self._selectedHandle
        setter = self._rect.__getattribute__("set" + handle)
        delta = QPointF(currentMouse - self._mouseOrigin)

        if handle in ("Left, Right"):
            setter(self._boundingRectPoint.x() + delta.x())
        elif handle in ("Top", "Bottom"):
            setter(self._boundingRectPoint.y() + delta.y())
        else:
            setter(self._boundingRectPoint + delta)

        self._rect = self._rect.normalized()
        self.resize.emit(self._rect)

        self._updateHandlePositions()
        self.update()

    def _boundingRectPointFromHandle(self) -> QPointF:

        """
        Return the bounding rectangle corresponding point based on the
        clicked handle
        """

        b = self.boundingRect()
        handle = self._selectedHandle

        if handle == "TopLeft":
            return QPointF(b.left(), b.top())
        if handle == "Left":
            return QPointF(b.left(), b.center().y())
        if handle == "BottomLeft":
            return QPointF(b.left(), b.bottom())
        if handle == "TopRight":
            return QPointF(b.right(), b.top())
        if handle == "Right":
            return QPointF(b.right(), b.center().y())
        if handle == "BottomRight":
            return QPointF(b.right(), b.bottom())
        if handle == "Top":
            return QPointF(b.center().x(), b.top())
        if handle == "Bottom":
            return QPointF(b.center().x(), b.bottom())

    def mouseMoveEvent(self, e: QMouseEvent) -> None:

        """Edit the object if the user clicked on a handle"""

        if self._selectedHandle is not None:
            self._performResize(e.scenePos())

        super().mouseMoveEvent(e)

    def mousePressEvent(self, e: QMouseEvent) -> None:

        """Capture clicked handle"""

        self._selectedHandle = self._handleAt(e.scenePos())

        if self._selectedHandle is not None:
            self._mouseOrigin = e.scenePos()
            self._boundingRectPoint = self._boundingRectPointFromHandle()

        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        self._selectedHandle = None

        super().mouseReleaseEvent(e)

    def hoverMoveEvent(self, e) -> None:
        super().hoverMoveEvent(e)

        print("hover")

    def paint(
        self,
        painter: QPainter,
        option,
        widget: QWidget = None,
    ) -> None:

        painter.setBrush(QBrush(QColor(70, 70, 70, 100)))
        painter.setPen(QPen(QColor(200, 200, 200, 100), 1.0, Qt.DashLine))
        painter.drawRect(self._rect)

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(Qt.transparent))
        painter.setPen(
            QPen(QColor(Qt.white), 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        )
        for handle, rect in self._handles.items():
            painter.drawRect(rect)

    # def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value: Any) -> Any:
    #     if change == QGraphicsItem.ItemPositionChange:

    #         print("change")

    #         delta: QPointF = value - self.pos()

    #         """ Resize ourselves"""
    #         self._rect = self._rect.adjusted(0, 0, delta.x(), delta.y())
    #         self.update()
    #         self._updateHandlePositions()

    #         limit = QPointF(
    #             self._resizable.scenePos().x(), self._resizable.scenePos().y()
    #         )
    #         value.setX(value.x() if value.x() > limit.x() else limit.x())
    #         value.setY(value.y() if value.y() > limit.y() else limit.y())

    #         """ resize by the delta movement"""
    #         self.resize.emit(value - self.pos())

    #         return value

    #     return super().itemChange(change, value)
