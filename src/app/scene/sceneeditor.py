from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QToolBar,
    QAction,
    QActionGroup,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsPixmapItem,
)
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QFileInfo, QRectF, QPointF
from PyQt5.QtGui import QPixmap
from app.object.rectangle import Rectangle
from .sceneview import SceneView
from .scenemodel import SceneModel


class SceneEditor(QMainWindow):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self._setupUi()
        self._setupToolBar()

    def _setupUi(self):
        self._scene: QGraphicsScene = SceneModel()
        self._view: QGraphicsView = SceneView(scene=self._scene, parent=self)
        self.setCentralWidget(self._view)

    def _setupToolBar(self):
        self._toolbar = self.addToolBar("tool")

        self._hotspot = QAction("Draw Hotspot", self)
        self._hotspot.setToolTip("Draw a box defining a hotspot")
        self._hotspot.triggered.connect(lambda: self._scene.setTool("DrawBoxTool"))
        self._hotspot.setCheckable(True)

        self._resize = QAction("Edit object", self)
        self._resize.setToolTip("Edit an object")
        self._resize.setCheckable(True)

        self._select = QAction("Select object", self)
        self._select.setToolTip("Select an object")
        self._select.triggered.connect(lambda: self._scene.setTool("SelectTool"))
        self._select.setCheckable(True)

        self._toolbar.addAction(self._hotspot)
        self._toolbar.addAction(self._resize)
        self._toolbar.addAction(self._select)

        group = QActionGroup(self)
        group.addAction(self._hotspot)
        group.addAction(self._resize)
        group.addAction(self._select)

    # TODO this implementation lacks robustness
    def setBackgroundImage(self, path: str) -> None:
        self._backgroundpath = path
        self._view.setBackgroundImage(QPixmap(path))

    # TODO implement proper per object serialization
    def serialize(self, path: str) -> None:
        with open(path, "wt", encoding="utf-8", newline="\n") as f:
            f.write(f"{self._backgroundpath}\n")

            for i, item in enumerate(self._scene.items()):
                if not isinstance(item, (Rectangle)):
                    continue

                f.write(f"{i}, {item.serialize()}\n")

    def deserialize(self, path: str) -> None:
        with open(path, "rt", encoding="utf-8", newline="\n") as f:
            lines = f.readlines()

            img = QFileInfo(lines[0].strip()).canonicalFilePath()
            self.setBackgroundImage(img)

            for line in lines[1:]:
                line = line.strip()
                if len(line) > 0:
                    item = Rectangle(
                        position=QPointF(0, 0),
                        rect=QRectF(0, 0, 0, 0),
                        scene=self._scene,
                    )
                    item.deserialize(line)
                    self._scene.addItem(item)

            """ set items not interactable by default"""
            self._scene.setItemsInteractivity(False)
