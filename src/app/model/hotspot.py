from PyQt5.QtCore import QObject, QPointF, pyqtSignal
from ..utils.serializable import Serializable


class HotSpotModel(QObject, Serializable):

    sigPositionChanged = pyqtSignal(float)

    def __init__(self):
        super().__init__(None)

        self._x: float = 0
        self._y: float = 0

    def setPosition(self, point: QPointF) -> None:
        self._x = point.x()
        self._y = point.y()

        self.sigPositionChanged.emit(self._x)

    def serialize(self) -> str:
        pass

    def deserialize(self, data: str) -> None:
        pass
