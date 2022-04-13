from PyQt5.QtWidgets import (
    QApplication,
    QDockWidget,
    QWidget,
    QTreeView,
    QFileSystemModel,
    QMenu,
    QVBoxLayout,
)
from PyQt5.QtCore import Qt, QEvent, QDir, pyqtSlot
from PyQt5.QtGui import QCursor


class FileBrowser(QDockWidget):
    def __init__(self, parent=None):
        super().__init__("Project Browser", parent=parent)

        self._setupUi()
        self._populate()

    def _setupUi(self) -> None:
        self.setContentsMargins(0, 0, 0, 0)
        self.treeview = QTreeView(self)
        self.treeview.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeview.customContextMenuRequested.connect(self.contextMenu)
        self.treeview.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setWidget(self.treeview)

    def _populate(self) -> None:
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
