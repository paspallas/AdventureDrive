from PyQt5.QtCore import Qt, QSignalMapper, QEvent, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QMdiArea, QWidget, QTabWidget

from ..scene.sceneeditor import SceneEditor
from ..script.scripteditor import ScriptEditor


class MdiContainer(QMdiArea):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setViewMode(QMdiArea.TabbedView)
        self.setTabsClosable(True)
        self.setTabsMovable(False)
        self.setTabPosition(QTabWidget.North)
        self._windowMapper = QSignalMapper(self)
        self._windowMapper.mapped[QWidget].connect(self._setActiveSubWindow)

    def createMdiChild(self, name: str) -> QWidget:
        if name == "scene":
            child = SceneEditor()
        elif name == "script":
            child = ScriptEditor()

        self.addSubWindow(child)
        return child

    @pyqtSlot()
    def _setActiveSubWindow(self, window: QWidget) -> None:
        if window:
            self.setActiveSubWindow(window)
