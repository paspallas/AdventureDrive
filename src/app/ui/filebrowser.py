from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QTreeView,
    QFileSystemModel,
    QMenu,
    QVBoxLayout,
)
from PyQt5.QtCore import Qt, QEvent, QDir, pyqtSlot
from PyQt5.QtGui import QCursor


class FileBrowser(QWidget):
    def __init__(self):
        super().__init__()

        self.setupUi()
        self.populate()

    def setupUi(self) -> None:
        self.vbox = QVBoxLayout()
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vbox)
        self.treeview = QTreeView(self)
        self.vbox.addWidget(self.treeview)

        self.treeview.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeview.customContextMenuRequested.connect(self.contextMenu)
        self.treeview.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

    def populate(self) -> None:
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.currentPath())
        self.treeview.setModel(self.model)
        # self.treeview.setRootIndex(self.model.index(path))
        self.treeview.setSortingEnabled(True)

    def contextMenu(self) -> None:
        menu = QMenu()
        menu.addAction("Open", self.openFile)
        menu.exec(QCursor().pos())

    @pyqtSlot()
    def openFile(self):
        index = self.treeview.currentIndex()
        filePath = self.model.filePath(index)
        import os

        os.startfile(filePath)


if __name__ == "__main__":
    import sys

    app = QApplication([])
    fb = FileBrowser()
    fb.setWindowTitle("File Browser")
    fb.show()
    sys.exit(app.exec())
