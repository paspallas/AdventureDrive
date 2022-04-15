from PyQt5.QtCore import QObject, pyqtSignal
from ..ui.propertyeditor import *


class DocumentModel(QObject):

    sigDocumentChanged = pyqtSignal(Node)

    def __init__(self):
        super().__init__(None)
        self._objects = list()

    def addObject(self, model, viewItem):
        viewItem.setModel(model)

        self._objects.append((model, viewItem))

        # create property tree for this item
        position = FloatSpinNode("x")
        model.sigPositionChanged.connect(position.sltSetValue)

        root = Node()
        root.addChild(position)

        self.sigDocumentChanged.emit(root)
