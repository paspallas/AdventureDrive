from PyQt5.QtCore import Qt, QEvent, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (
    QWidget,
    QGraphicsView,
    QGraphicsScene,
    QFrame,
    QSizePolicy,
    QStyleOptionGraphicsItem,
    QGraphicsItem,
    QGraphicsPixmapItem,
)
from PyQt5.QtGui import (
    QPainter,
    QMouseEvent,
    QWheelEvent,
    QKeyEvent,
    QPixmap,
)
from app.ui.statusbar import StatusBar
from .scenemodel import SceneModel

kZoomFactor = 1.2
kZoomMax = 25
kZoomMin = 0.5


class SceneView(QGraphicsView):
    def __init__(
        self,
        parent: QWidget = None,
        scene: QGraphicsScene = None,
        background: QPixmap = None,
    ):
        super().__init__(parent)

        self._scene: QGraphicsScene = scene if scene else SceneModel()
        self.setScene(self._scene)
        self._background = QGraphicsPixmapItem()

        self._setupUi(background)
        self._notifyZoomChange(1)

    @property
    def scene(self) -> QGraphicsScene:
        return self._scene

    def _setupUi(self, background: QPixmap = None) -> None:
        self.setFrameStyle(QFrame.NoFrame)
        self.setContentsMargins(0, 0, 0, 0)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setRenderHints(
            QPainter.Antialiasing
            | QPainter.HighQualityAntialiasing
            | QPainter.TextAntialiasing
            | QPainter.SmoothPixmapTransform
        )

        if background:
            self.setBackgroundImage(background)

    def setBackgroundImage(self, pixmap: QPixmap) -> None:
        self._background.setPixmap(pixmap)
        self._background.setFlag(QGraphicsItem.ItemIsMovable, False)
        self._background.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self._scene.addItem(self._background)

        # adjust the scene rect size to the background image rect
        rect = self._background.boundingRect()
        self._scene.setSceneRect(rect.x(), rect.y(), rect.width(), rect.height())
        self.fitInView(self._background, Qt.KeepAspectRatio)

    def resizeEvent(self, e: QEvent) -> None:
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

    @pyqtSlot()
    def resetZoomLevel(self) -> None:
        self.resetTransform()
        self.update()
        self._notifyZoomChange(1)
