from PyQt5.QtWidgets import (
    QWidget,
    QGraphicsScene,
    QGraphicsObject,
    QGraphicsItem,
    QGraphicsSceneMouseEvent,
    QGraphicsSceneHoverEvent,
)
from PyQt5.QtGui import QPainter, QPainterPath, QPen, QColor, QBrush
from PyQt5.QtCore import Qt, QRectF, QLineF, QPointF, pyqtSignal
from typing import Any, Dict
from .rectangle import Rectangle


class EditGizmo(QGraphicsObject):

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

        self._handleSize = 2

        self._mouseOrigin: QPointF = None
        self._boundingRectPoint: QPointF = None
        self._selectedHandle: str = None
        self._handles: Dict[str, QRectF] = {}

        flags = QGraphicsItem.ItemSendsGeometryChanges | QGraphicsItem.ItemIsFocusable
        self.setFlags(flags)
        self.setVisible(True)
        self.setAcceptHoverEvents(True)
        self.setZValue(10000)

        """ Place the resizer gizmo over the resizable object"""
        self.setPos(self._resizable.scenePos())
        self._updateHandlePositions()

        """ Manipulate resizable object """
        self.resize.connect(lambda change: self._resizable.resize(change))
        self.positionChange.connect(lambda change: self._resizable.position(change))

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
        s = self._handleSize
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

    def onMouseMoveEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        if self._selectedHandle is not None:
            self._updateItemSize(e)
        elif e.buttons() & Qt.LeftButton:
            self._updateItemPosition(e)

    def onMousePressEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        self._selectedHandle = self._handleAt(e.scenePos())

        if self._selectedHandle is not None:
            self._mouseOrigin = e.scenePos()
            self._boundingRectPoint = self._boundingRectPointFromHandle(
                self._selectedHandle
            )

    def onMouseReleaseEvent(self, e: QGraphicsSceneMouseEvent) -> None:
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

        brush = QBrush(QBrush(QColor(70, 70, 70, 120)))
        painter.setBrush(brush)
        painter.drawRect(self._rect)

        painter.setRenderHint(QPainter.Antialiasing)
        brush.setColor(QColor(Qt.transparent))
        painter.setBrush(brush)
        pen = QPen(QColor(Qt.white), 0, Qt.DashLine, Qt.RoundCap, Qt.RoundJoin)
        pen.setCosmetic(True)
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

        o = self._handleSize
        return self._rect.adjusted(-o, -o, o, o)

    def shape(self) -> QPainterPath:
        path = QPainterPath()
        path.addRect(self._rect)

        for shape in self._handles.values():
            path.addEllipse(shape)

        return path
