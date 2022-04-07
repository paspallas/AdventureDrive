from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QToolBar,
    QAction,
    QActionGroup,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsItem,
    QGraphicsPixmapItem,
)
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QFileInfo, QRectF, QPointF
from PyQt5.QtGui import QPixmap
from app.object.rectangle import Rectangle
from app.object.sprite import Sprite
from .sceneview import SceneView
from .scenemodel import SceneModel


class SceneEditor(QMainWindow):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self._setupUi()
        self._setupToolBar()

        # TODO test
        self._sprite = Sprite()
        self._sprite.setPixmap(
            QPixmap("F:/devel/sega/berlin/AdventureDrive/serpiente.PNG").copy(
                8, 10, 42, 61
            )
        )
        self._sprite.setPos(10, 10)
        self._scene.addItem(self._sprite)

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

        self._edit = QAction("Edit object", self)
        self._edit.setToolTip("Edit an object")
        self._edit.triggered.connect(lambda: self._scene.setTool("EditObjectTool"))
        self._edit.setCheckable(True)

        self._delete = QAction("Delete object", self)
        self._delete.setToolTip("Delete and object")
        self._delete.triggered.connect(lambda: self._scene.setTool("DeleteObjectTool"))
        self._delete.setCheckable(True)

        self._toolbar.addAction(self._hotspot)
        self._toolbar.addAction(self._edit)
        self._toolbar.addAction(self._delete)

        group = QActionGroup(self)
        group.addAction(self._hotspot)
        group.addAction(self._edit)
        group.addAction(self._delete)

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
                    )
                    item.deserialize(line)
                    self._scene.addItem(item)
