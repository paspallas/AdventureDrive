from PyQt5.QtCore import QPointF, QRectF
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QMouseEvent
from app.object.rectangle import Rectangle
from .abstracttool import AbstractTool

hintsize = 16


class DrawBoxTool(AbstractTool):
    def __init__(self, scene: QGraphicsScene = None):
        super().__init__(scene=scene)

    def enable(self):
        pass

    def disable(self):
        if self._item:
            self._scene.removeItem(self._item)

    def onMouseMove(self, e: QMouseEvent) -> None:
        x, y = (e.scenePos().x(), e.scenePos().y())

        if not self._item and not self._origin:
            """Show a rectangle of fixed size to hint the user"""
            self._item = Rectangle(
                position=QPointF(x, y),
                rect=QRectF(0, 0, hintsize, hintsize),
                scene=self._scene,
            )
            self._scene.addItem(self._item)

        elif self._item and not self._origin:
            """Move the hinting rectangle"""
            self._item.setPos(x, y)

        elif self._item and self._origin:
            """Draw the final rectangle"""
            sizex, sizey = (x - self._origin.x(), y - self._origin.y())
            sizex, sizey = (sizex if sizex > 0 else 1, sizey if sizey > 0 else 1)

            self._item.setRect(QRectF(0, 0, sizex, sizey).normalized())

    def onMousePress(self, e: QMouseEvent) -> None:
        """Capture drawing start position"""
        self._origin = e.scenePos()

    def onMouseRelease(self, e: QMouseEvent) -> None:
        """Finish drawing"""
        self._item = None
        self._origin = None

    def onMouseDoubleClick(self, e: QMouseEvent):
        pass
