from PyQt5.QtCore import Qt, QEvent, QPointF, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (
    QWidget,
    QGraphicsView,
    QGraphicsScene,
    QFrame,
    QSizePolicy,
    QStyleOptionGraphicsItem,
    QGraphicsItem,
    QGraphicsPixmapItem,
    QOpenGLWidget,
)
from PyQt5.QtGui import (
    QPainter,
    QMouseEvent,
    QWheelEvent,
    QHoverEvent,
    QKeyEvent,
    QResizeEvent,
    QPixmap,
    QSurfaceFormat,
)
from app.ui.statusbar import StatusBar
from .scenemodel import SceneModel
from app.object.background import BackGround

kZoomFactor = 1.2
kZoomMax = 40
kZoomMin = 0.5


class SceneView(QGraphicsView):
    def __init__(
        self,
        background: QPixmap = None,
        parent: QWidget = None,
        scene: QGraphicsScene = None,
    ):
        super().__init__(parent)

        self.setScene(scene)
        self._background = BackGround()

        self._setupUi()
        self.setMouseTracking(True)
        self._notifyZoomChange(1)

    def _setupUi(self) -> None:
        self.setFrameStyle(QFrame.NoFrame)
        self.setContentsMargins(0, 0, 0, 0)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCacheMode(QGraphicsView.CacheBackground)

        # fmt = QSurfaceFormat()
        # fmt.setSamples(1)
        # gl = QOpenGLWidget()
        # gl.setFormat(fmt)
        # self.setViewport(gl)
        # self.setRenderHints(
        #     QPainter.Antialiasing
        #     | QPainter.TextAntialiasing
        #     | QPainter.SmoothPixmapTransform
        # )

    def setBackgroundImage(self, pixmap: QPixmap) -> None:
        self._background.setPixmap(pixmap)
        self.scene().addItem(self._background)
        self._background.enableGrid()
        self.scene().setFocusedItem(self._background.grid)

        # Add extra space around the scene background. This gives the user a more pleasant
        # navigation experience

        extraPx = 480
        rect = self._background.boundingRect().adjusted(
            -extraPx, -extraPx / 2, extraPx, extraPx / 2
        )

        self.scene().setSceneRect(rect)
        self.fitInView(self._background, Qt.KeepAspectRatio)

    def _enableViewPortPan(self, e: QMouseEvent) -> None:
        """by default QGraphicsView uses the left mouse button to perform panning
         we are going to create a left mouse button press event whenever we press
        the middle mouse button to fake the desired behaviour
        """

        # in case left mouse was pressed fake a release event
        releaseLeftMouseEvent = QMouseEvent(
            QEvent.MouseButtonRelease,
            e.localPos(),
            e.screenPos(),
            Qt.LeftButton,
            Qt.NoButton,
            e.modifiers(),
        )
        super().mouseReleaseEvent(releaseLeftMouseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

        # now we create the press event to trick QGraphicsView
        pressLeftMouseEvent = QMouseEvent(
            e.type(),
            e.localPos(),
            e.screenPos(),
            Qt.LeftButton,
            e.buttons() | Qt.LeftButton,
            e.modifiers(),
        )
        super().mousePressEvent(pressLeftMouseEvent)

    def _disableViewPortPan(self, e: QMouseEvent) -> None:
        # fake a left mouse button release event
        releaseLeftMouseEvent = QMouseEvent(
            e.type(),
            e.localPos(),
            e.screenPos(),
            Qt.LeftButton,
            e.buttons() & ~Qt.LeftButton,
            e.modifiers(),
        )
        super().mousePressEvent(releaseLeftMouseEvent)
        self.setDragMode(QGraphicsView.NoDrag)

    def _setZoom(self, factor: float, levelOfDetail: float) -> None:
        self.scale(factor, factor)
        self._notifyZoomChange(levelOfDetail)

    def _notifyZoomChange(self, levelOfDetail: float) -> None:
        StatusBar().bar.showMessage(f"Zoom { round(levelOfDetail * 100) }%")

    def wheelEvent(self, e: QWheelEvent) -> None:
        if e.modifiers() & Qt.Modifier.CTRL:

            lod = QStyleOptionGraphicsItem.levelOfDetailFromTransform(self.transform())

            if e.angleDelta().y() > 0:
                if lod * kZoomFactor < kZoomMax:
                    self._setZoom(kZoomFactor, lod * kZoomFactor)
                else:
                    allowableFactor = kZoomMax / lod
                    self._setZoom(allowableFactor, kZoomMax)

            elif e.angleDelta().y() < 0:
                if lod * (1 / kZoomFactor) > kZoomMin:
                    self._setZoom(1 / kZoomFactor, lod / kZoomFactor)
                else:
                    allowableFactor = kZoomMin / lod
                    self._setZoom(allowableFactor, kZoomMin)
        else:
            super().wheelEvent(e)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        if e.buttons() & Qt.MiddleButton:
            self._enableViewPortPan(e)
        else:
            super().mousePressEvent(e)

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        if e.button() == Qt.MiddleButton:
            self._disableViewPortPan(e)
        else:
            super().mouseReleaseEvent(e)

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        s: QPointF = self.mapToScene(e.pos())
        StatusBar().bar.showMessage(f"({int(s.x())}, {int(s.y())})")

        super().mouseMoveEvent(e)

    def resizeEvent(self, e: QResizeEvent) -> None:
        rect = self.scene().getFocusedItemRect()

        if rect is not None:
            self.fitInView(rect, Qt.KeepAspectRatio)
        else:
            self.fitInView(self._background, Qt.KeepAspectRatio)

    @pyqtSlot()
    def resetZoomLevel(self) -> None:
        self.resetTransform()
        self.update()
        self._notifyZoomChange(1)
