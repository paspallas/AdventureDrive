from PyQt5.QtWidgets import (
    QWidget,
    QGraphicsScene,
    QGraphicsObject,
    QGraphicsItem,
    QGraphicsSceneMouseEvent,
    QGraphicsSceneHoverEvent,
)
from PyQt5.QtGui import QPainter, QPainterPath, QPen, QColor, QBrush
from PyQt5.QtCore import Qt, QRectF, QLineF, QPointF, QTimer, pyqtSignal
from typing import Any, Dict
from .rectangle import Rectangle


class EditGizmo(QGraphicsObject):

    resize = pyqtSignal(QRectF, name="resize")
    positionChange = pyqtSignal(QPointF, name="positionChange")

    HANDLE_SIZE = 1.5

    def __init__(
        self,
        parent: QWidget = None,
        editable: Rectangle = None,
    ):
        super().__init__(parent)

        self._editable = editable
        self._rect: QRectF = editable.rect()

        self._mouseOrigin: QPointF = None
        self._boundingRectPoint: QPointF = None
        self._selectedHandle: str = None
        self._handles: Dict[str, QRectF] = {}

        flags = (
            QGraphicsItem.ItemSendsGeometryChanges
            | QGraphicsItem.ItemIsFocusable
            | QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemIsMovable
        )
        self.setFlags(flags)
        self.setVisible(True)
        self.setAcceptHoverEvents(True)
        self.setZValue(10000)

        """ Dash line animation """
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._updateDashLineAnimation)
        self.timer.setInterval(120)
        self.timer.start()
        self.dashOffset = 0.0

        """ Place the resizer gizmo over the editable object"""
        self.setPos(self._editable.scenePos())
        self._updateHandlePositions()

        """ Manipulate editable object """
        self.resize.connect(lambda change: self._editable.resize(change))
        self.positionChange.connect(lambda change: self._editable.position(change))

        self._cursors = {
            "TopLeft": Qt.SizeFDiagCursor,
            "Top": Qt.SizeVerCursor,
            "TopRight": Qt.SizeBDiagCursor,
            "Left": Qt.SizeHorCursor,
            "Right": Qt.SizeHorCursor,
            "BottomLeft": Qt.SizeBDiagCursor,
            "Bottom": Qt.SizeVerCursor,
            "BottomRight": Qt.SizeFDiagCursor,
        }

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
        s = self.HANDLE_SIZE
        b = self._rect

        """ Center the handles in the corners of the bounding rect """
        self._handles["TopLeft"] = QRectF(b.left() - s, b.top() - s, s, s)
        self._handles["Left"] = QRectF(b.left() - s - 0.5, b.center().y() - s / 2, s, s)
        self._handles["BottomLeft"] = QRectF(b.left() - s, b.bottom(), s, s)
        self._handles["TopRight"] = QRectF(b.right(), b.top() - s, s, s)
        self._handles["Right"] = QRectF(b.right() + 0.5, b.center().y() - s / 2, s, s)
        self._handles["BottomRight"] = QRectF(b.right(), b.bottom(), s, s)
        self._handles["Top"] = QRectF(b.center().x() - s / 2, b.top() - s - 0.5, s, s)
        self._handles["Bottom"] = QRectF(b.center().x() - s / 2, b.bottom() + 0.5, s, s)

    def _adjustRectWarp(self, handle: str, rect: QRectF) -> QRectF:
        lim = 0.5

        if rect.width() < lim:
            if handle in ("Left, TopLeft, BottomLeft"):
                rect.setLeft(rect.right() - lim)
            else:
                rect.setRight(rect.left() + lim)

        if rect.height() < lim:
            if handle in ("Top, TopLeft, TopRight"):
                rect.setTop(rect.bottom() - lim)
            else:
                rect.setBottom(rect.top() + lim)

        return rect

    def _updateItemSize(self, e: QGraphicsSceneMouseEvent) -> None:
        self.prepareGeometryChange()

        delta = QPointF(e.scenePos() - self._mouseOrigin)
        handle = self._selectedHandle
        setter = self._rect.__getattribute__("set" + handle)

        if handle in ("Left, Right"):
            setter(self._boundingRectPoint.x() + delta.x())
        elif handle in ("Top", "Bottom"):
            setter(self._boundingRectPoint.y() + delta.y())
        else:
            setter(self._boundingRectPoint + delta)

        self._rect = self._adjustRectWarp(handle, self._rect)

        self._updateHandlePositions()
        self.resize.emit(self._rect)

    def _updateItemPosition(self, e: QGraphicsSceneMouseEvent) -> None:
        self.prepareGeometryChange()

        delta = QPointF(e.scenePos() - e.lastScenePos())
        self._rect.translate(delta)
        self.update(self._rect)
        self._updateHandlePositions()

        self.positionChange.emit(delta)

    def _boundingRectPointFromHandle(self, handle: str) -> QPointF:

        """
        Return the bounding rectangle corresponding point for the clicked handle
        """

        b = self._rect

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

    def _updateDashLineAnimation(self) -> None:
        self.dashOffset -= 1
        self.update()

    def mouseMoveEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        if self._selectedHandle is not None:
            self._updateItemSize(e)
        elif e.buttons() & Qt.LeftButton:
            self._updateItemPosition(e)

    def mousePressEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        self._selectedHandle = self._handleAt(e.scenePos())

        if self._selectedHandle is not None:
            self._mouseOrigin = e.scenePos()
            self._boundingRectPoint = self._boundingRectPointFromHandle(
                self._selectedHandle
            )

    def mouseReleaseEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        self._selectedHandle = None
        self._mouseOrigin = None

    def hoverMoveEvent(self, e: QGraphicsSceneHoverEvent) -> None:
        handle = self._handleAt(e.scenePos())
        cursor = Qt.SizeAllCursor if handle is None else self._cursors[handle]
        self.setCursor(cursor)

        super().hoverMoveEvent(e)

    def paint(
        self,
        painter: QPainter,
        option,
        widget: QWidget = None,
    ) -> None:

        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(QColor(Qt.transparent), 0, Qt.DashLine, Qt.RoundCap, Qt.RoundJoin)
        brush = QBrush(QBrush(QColor(70, 70, 70, 180)))

        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawRect(self._rect)

        brush.setColor(QColor(Qt.transparent))
        painter.setBrush(brush)

        pen.setBrush(Qt.white)
        pen.setDashOffset(self.dashOffset)
        painter.setPen(pen)
        painter.drawRect(self._rect)

        brush.setColor(QColor(Qt.white))
        pen.setColor(QColor(0, 0, 0))
        pen.setStyle(Qt.SolidLine)
        painter.setPen(pen)
        painter.setBrush(brush)

        for rect in self._handles.values():
            painter.drawEllipse(rect)

        c: QPointF = self._rect.center()

        cross = [
            QLineF(c.x() - 2, c.y(), c.x() + 2, c.y()),
            QLineF(c.x(), c.y() - 2, c.x(), c.y() + 2),
        ]

        painter.drawLines(*cross)

    def boundingRect(self) -> QRectF:

        """Adjust the bounding rect so that it contains the handles"""

        o = self.HANDLE_SIZE
        return self._rect.adjusted(-o, -o, o, o)

    def shape(self) -> QPainterPath:
        path = QPainterPath()
        path.addRect(self._rect)

        for shape in self._handles.values():
            path.addEllipse(shape)

        return path
