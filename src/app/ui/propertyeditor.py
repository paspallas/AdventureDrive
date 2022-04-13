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
from PyQt5.QtCore import Qt, QEvent, QObject, QAbstractItemModel, pyqtSlot, pyqtSignal


class Node(QObject):
    def __init__(self, property_: str, widget: QWidget = None):
        super().__init__(None)

        self._property = property_
        self.item = QTreeWidgetItem(None, [property_]) if property_ != "root" else None
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


class PropertyEditor(QDockWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__("Property Editor", parent)

        self._setupUi()

        # tree structure
        root = Node("root")
        root.addChild(Node("Name", QLineEdit()))
        root[0].addChild(Node("first name", QLineEdit()))
        root[0][0].addChild(Node("Age", QSpinBox()))
        root[0][0].addChild(Node("Minor", QSpinBox()))
        root[0][0][0].addChild(Node("Hair", QLabel("Brown")))
        root[0][0][1].addChild(Node("Eyes", QLabel("Blue")))

        root.addChild(Node("Position", QLabel("( , )"))).addChildren(
            [Node("x", QSpinBox()), Node("y", QSpinBox())]
        )
        root.addChild(Node("Color", QPushButton("color")))

        self._traverse(root)

    def setModel(self, tree: Node) -> None:
        self._model = tree
        self._traverse(tree)

    def _traverse(self, node: Node) -> None:
        for i, childnode in enumerate(node):
            self._tree.insertTopLevelItem(i, childnode.item)
            self._tree.setItemWidget(childnode.item, 1, childnode.widget)

            for node in childnode:
                self._innertraverse(node)

    def _innertraverse(self, node: Node) -> None:
        if node is None:
            return

        for childnode in node:
            self._innertraverse(childnode)

        self._tree.setItemWidget(node.item, 1, node.widget)

    def _setupUi(self) -> None:
        self._tree = QTreeWidget(self)
        self._tree.setColumnCount(2)
        self._tree.setHeaderLabels(("Property", "Value"))
        self.setWidget(self._tree)
