from PyQt5.QtWidgets import QWidget, QGraphicsItem, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
from app.utils.serializable import Serializable


class Sprite(QGraphicsPixmapItem, Serializable):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent=parent)

        flags = (
            QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemIsMovable
            | QGraphicsItem.ItemIsFocusable
            | QGraphicsItem.ItemSendsScenePositionChanges
        )
        self.setFlags(flags)
        self.setAcceptHoverEvents(True)

    def serialize(self) -> str:
        pass

    def deserialize(self, data: str) -> None:
        pass
