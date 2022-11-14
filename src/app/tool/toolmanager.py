from PyQt5.QtCore import Qt, QCoreApplication, QObject, QEvent, pyqtSlot
from PyQt5.QtWidgets import QGraphicsScene
from importlib import import_module as imodule
from .abstracttool import AbstractTool


class ToolManager(QObject):

    """
    This class manages tool operations in the graphics scene by intercepting all
    events that the graphicsview sends to the scene. The events are always forwarded
    to the scene so that graphics items can receive them.
    """

    def __init__(self, scene: QGraphicsScene) -> None:
        super().__init__(scene)

        self._tool: AbstractTool = None
        scene.installEventFilter(self)

    def eventFilter(self, obj: QObject, e: QEvent) -> bool:
        scene: QGraphicsScene = obj

        if scene is None:
            return super().eventFilter(obj, e)

        if e.type() == QEvent.GraphicsSceneMousePress:
            if self._tool is not None:
                if scene._editableAreaRect.contains(e.scenePos()):
                    self._tool.onMousePress(e)

            return False

        elif e.type() == QEvent.GraphicsSceneMouseMove:
            if self._tool is not None:
                if scene._editableAreaRect.contains(e.scenePos()):
                    self._tool.onMouseMove(e)

            return False

        elif e.type() == QEvent.GraphicsSceneMouseRelease:
            if self._tool is not None:
                if scene._editableAreaRect.contains(e.scenePos()):
                    self._tool.onMouseRelease(e)

            return False

        return super().eventFilter(obj, e)

    @pyqtSlot(str)
    def setTool(self, tool: str, checked: bool) -> None:
        # Disable current tool
        if self._tool is not None and not checked:
            self._tool.disable()
            self._tool = None
            return

        # Change current tool
        if self._tool is not None and checked:
            self._tool.disable()
            self._tool = None

        try:
            Tool = getattr(imodule(f"app.tool.{tool}".lower()), tool)
            self._tool = Tool(scene=self.parent())
            self._tool.enable()
        except AttributeError as e:
            print(e)
