from PyQt5.QtCore import Qt, QSignalMapper, QEvent, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QMdiArea, QWidget, QTabWidget

from app.scene.sceneeditor import SceneEditor
from .statusbar import StatusBar


class MdiContainer(QMdiArea):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setViewMode(QMdiArea.TabbedView)
        self.setTabsClosable(True)
        self.setTabsMovable(True)
        self.setTabPosition(QTabWidget.North)
        self._windowMapper = QSignalMapper(self)
        self._windowMapper.mapped[QWidget].connect(self._setActiveSubWindow)

    def createMdiChild(self, name: str = None) -> QWidget:
        # TODO create editor subwindow based on the file type
        child = SceneEditor()

        # self.resetZoomLevel.connect(child.resetZoomLevel)
        self.addSubWindow(child)

        return child

    @pyqtSlot()
    def _setActiveSubWindow(self, window: QWidget) -> None:
        if window:
            self.setActiveSubWindow(window)
