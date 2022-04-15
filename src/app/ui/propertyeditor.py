from PyQt5.QtWidgets import (
    QDockWidget,
    QWidget,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QSpinBox,
    QDoubleSpinBox,
)
from PyQt5.QtCore import Qt, QEvent, QObject, pyqtSlot, pyqtSignal

__all__ = ["Node", "FloatSpinNode"]


class Node(QObject):
    def __init__(self, property_: str = None, widget: QWidget = None):
        super().__init__(None)

        self._property = property_
        self.item = QTreeWidgetItem(None, [property_]) if property_ else None
        self.widget = widget

        self._children = list()
        self._index = 0

    def addChild(self, child):
        self._children.append(child)

        if self.item is not None:
            self.item.addChild(child.item)

        return child

    def addChildren(self, children: list()) -> None:
        self._children.extend(children)

        if self.item is not None:
            for child in children:
                self.item.addChild(child.item)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            result = self._children[self._index]

        except IndexError:
            raise StopIteration

        self._index += 1
        return result

    def __len__(self):
        return len(self._children)

    def __getitem__(self, index):
        return self._children[index]

    def __setitem__(self, index, item):
        self._children[index] = item


class TextNode(Node):
    def __init__(self, property_: str):
        super().__init__(property_, QLineEdit())


class FloatSpinNode(Node):

    sigValueChanged = pyqtSignal(float)

    def __init__(self, property_: str):
        super().__init__(property_, QDoubleSpinBox())

        self.widget.valueChanged.connect(self.sigValueChanged)
        self.widget.setRange(0, 9999)

    def sltSetValue(self, value: float) -> None:
        self.widget.setValue(value)


class IntSpinNode(Node):
    def __init__(self, property_: str):
        super().__init__(property_, QSpinBox())


class ButtonNode(Node):
    def __init__(self, property_: str):
        super().__init__(property_, QPushButton(property_))


class LabelNode(Node):
    def __init__(self, property_: str):
        super().__init__(property_, QLabel())


class PropertyEditor(QDockWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__("Property Editor", parent)

        self._setupUi()

        # root = Node()
        # root.addChild(TextNode("Name"))
        # root.addChild(LabelNode("Position")).addChildren(
        #     [FloatSpinNode("x"), FloatSpinNode("y")]
        # )
        # root.addChild(ButtonNode("Color"))

        # self._traverse(root)

    @pyqtSlot(Node)
    def sltSetModel(self, tree: Node) -> None:
        self._model = tree
        self._traverse(tree)

    def _traverse(self, node: Node) -> None:
        for i, childNode in enumerate(node):
            self._tree.insertTopLevelItem(i, childNode.item)
            self._tree.setItemWidget(childNode.item, 1, childNode.widget)

            for subChildNode in childNode:
                self._innertraverse(subChildNode)

    def _innertraverse(self, node: Node) -> None:
        if node is None:
            return

        for childNode in node:
            self._innertraverse(childNode)

        self._tree.setItemWidget(node.item, 1, node.widget)

    def _setupUi(self) -> None:
        self._tree = QTreeWidget(self)
        self._tree.setColumnCount(2)
        self._tree.setHeaderLabels(("Property", "Value"))
        self.setWidget(self._tree)
