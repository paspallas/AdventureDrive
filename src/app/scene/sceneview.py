from PyQt5.QtCore import Qt, QEvent, QPointF, QCoreApplication, pyqtSignal, pyqtSlot
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
    QGraphicsSceneMouseEvent,
)
from PyQt5.QtGui import (
    QPainter,
    QMouseEvent,
    QWheelEvent,
    QKeyEvent,
    QResizeEvent,
    QPixmap,
    QSurfaceFormat,
    QCursor,
)
from ..uitools.pancontroller import PanController
from ..uitools.zoomcontroller import ZoomController
from ..ui.statusbar import StatusBar
from ..object.background import BackGround
from .scenemodel import SceneModel


class SceneView(QGraphicsView):
    def __init__(
        self,
        parent: QWidget = None,
        scene: QGraphicsScene = None,
    ):
        super().__init__(parent)

        PanController(self)
        ZoomController(self)

        self.setScene(scene)
        self.setFrameStyle(QFrame.NoFrame)
        self.setContentsMargins(0, 0, 0, 0)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMouseTracking(True)

        self.background = BackGround()

    def setBackgroundImage(self, pixmap: QPixmap) -> None:
        self.background.setPixmap(pixmap)
        self.scene().addItem(self.background)
        self.background.enableGrid()
        self.scene().setEditableAreaRect(self.background.boundingRect())

        # Add extra space around the scene background. Give the user a more pleasant
        # navigation experience

        extraPx = 240
        rect = self.background.boundingRect().adjusted(
            -extraPx, -extraPx, extraPx, extraPx
        )

        self.scene().setSceneRect(rect)
        self.fitInView(self.background, Qt.KeepAspectRatio)

    def resizeEvent(self, e: QResizeEvent) -> None:
        self.fitInView(self.background, Qt.KeepAspectRatio)

    #     rect = self.scene().getFocusedItemRect()

    #     if rect is not None:
    #         self.fitInView(rect, Qt.KeepAspectRatio)
    #     else:
    #         self.fitInView(self.background, Qt.KeepAspectRatio)

    @pyqtSlot()
    def enableOpenGL():
        fmt = QSurfaceFormat()
        fmt.setSamples(2)
        gl = QOpenGLWidget()
        gl.setFormat(fmt)
        self.setViewport(gl)
        self.setRenderHints(
            QPainter.Antialiasing
            | QPainter.TextAntialiasing
            | QPainter.SmoothPixmapTransform
        )
