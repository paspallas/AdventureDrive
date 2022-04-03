from abc import ABC, ABCMeta, abstractmethod
from PyQt5.QtWidgets import QGraphicsItem


class SerdesWidget(ABCMeta, type(QGraphicsItem)):
    pass


class Serializable(ABC, metaclass=SerdesWidget):
    @classmethod
    @abstractmethod
    def serialize(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def deserialize(self, data: str) -> None:
        pass
