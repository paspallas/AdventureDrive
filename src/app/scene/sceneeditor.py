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
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QFileInfo, QRectF, QPointF
from PyQt5.QtGui import QPixmap, QIcon
from ..object.rectangle import Rectangle
from ..object.sprite import Sprite
from ..tool.toolmanager import ToolManager
from .sceneview import SceneView
from .scenemodel import SceneModel
import app.resources


class SceneEditor(QMainWindow):
    def __init__(self, document, parent: QWidget = None):
        super().__init__(parent)

        self._toolmanager = None

        self._setupUi(document)
        self._setupToolBar()

    def _setupUi(self, document):
        self._scene: QGraphicsScene = SceneModel(document)
        self._view: QGraphicsView = SceneView(scene=self._scene, parent=self)
        self.setCentralWidget(self._view)
        self._toolmanager = ToolManager(scene=self._scene)

    def _setupToolBar(self):
        toolbar = QToolBar(self)
        self.addToolBar(Qt.LeftToolBarArea, toolbar)
        toolbar.setAllowedAreas(Qt.LeftToolBarArea)
        toolbar.setOrientation(Qt.Vertical)
        toolbar.setMovable(False)

        hotspot = QAction(QIcon(":/icon/pencil"), "Draw Hotspot", self)
        hotspot.setToolTip("Draw Hotspot (H)")
        hotspot.triggered.connect(
            lambda checked: self._toolmanager.setTool("DrawBoxTool", checked)
        )
        hotspot.setCheckable(True)
        hotspot.setShortcut("H")
        hotspot.setAutoRepeat(False)

        polygon = QAction(QIcon(":/icon/polygon"), "Draw Polygon", self)
        polygon.setToolTip("Draw Polygon (P)")
        polygon.triggered.connect(
            lambda checked: self._toolmanager.setTool("PolygonTool", checked)
        )
        polygon.setCheckable(True)
        polygon.setShortcut("P")
        polygon.setAutoRepeat(False)

        edit = QAction(QIcon(":/icon/selection"), "Edit object", self)
        edit.setToolTip("Edit Object (E)")
        edit.triggered.connect(
            lambda checked: self._toolmanager.setTool("EditObjectTool", checked)
        )
        edit.setCheckable(True)
        edit.setShortcut("E")
        edit.setAutoRepeat(False)

        delete = QAction(QIcon(":/icon/eraser"), "Delete object", self)
        delete.setToolTip("Delete Object (D)")
        delete.triggered.connect(
            lambda checked: self._toolmanager.setTool("DeleteObjectTool", checked)
        )
        delete.setCheckable(True)
        delete.setShortcut("D")
        delete.setAutoRepeat(False)

        toolbar.addAction(hotspot)
        toolbar.addAction(polygon)
        toolbar.addAction(edit)
        toolbar.addAction(delete)

        group = QActionGroup(self)
        group.setExclusionPolicy(QActionGroup.ExclusionPolicy.ExclusiveOptional)
        group.addAction(hotspot)
        group.addAction(edit)
        group.addAction(delete)
        group.addAction(polygon)

    # TODO this implementation lacks robustness
    def setBackgroundImage(self, path: str) -> None:
        self._backgroundpath = path
        self._view.setBackgroundImage(QPixmap(path))

        # self._sprite = Sprite()
        # self._sprite.setPixmap(
        #     QPixmap("F:/devel/sega/berlin/AdventureDrive/serpiente.PNG").copy(
        #         8, 10, 42, 61
        #     )
        # )
        # self._sprite.setPos(10, 10)
        # self._scene.addItem(self._sprite)

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
