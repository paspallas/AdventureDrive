from PyQt5.QtCore import Qt, QSize, QEvent, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import (
    QMainWindow,
    QMenuBar,
    QMenu,
    QAction,
    QDockWidget,
    QWidget,
    QToolBar,
)
from PyQt5.QtGui import QKeySequence
from app.utils.action import *
from app.utils.fileio import FileIOControl
from app.utils.settings import SettingsManager
from app.script.scripteditor import ScriptEditor
from app.scene.sceneeditor import SceneEditor
from .statusbar import StatusBar
from .mdicontainer import MdiContainer


class MainWindow(QMainWindow):

    resetZoomLevel = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Adventure Drive")
        self._setupUi()
        self.setStatusBar(StatusBar().bar)
        SettingsManager().read(self)

    def _setupUi(self):
        self.setMinimumSize(QSize(800, 600))
        self._mdiArea = MdiContainer(self)
        self.setCentralWidget(self._mdiArea)

        self._createMenus()
        StatusBar().bar.showMessage("Ready", 4000)

        # self._editScript()

    #! TO DISABLE menu entries use action.setEnable(False)
    def _createMenus(self):
        menubar = self.menuBar()
        file = menubar.addMenu("&File")
        edit = menubar.addMenu("&Edit")

        file.addActions(
            [
                createAction(
                    "&New",
                    self._new,
                    shortcut=QKeySequence.New,
                    tip="Create a new scene",
                    parent=self,
                ),
                createAction(
                    "&Open",
                    self._open,
                    shortcut=QKeySequence.Open,
                    tip="Open an existing scene",
                    parent=self,
                ),
                createAction(
                    "&Save",
                    self._save,
                    shortcut=QKeySequence.Save,
                    tip="Save currently selected scene to disk",
                    parent=self,
                ),
                createAction(
                    "Save &As...",
                    None,
                    shortcut=QKeySequence.StandardKey.SaveAs,
                    tip="Save currently selected scene under a new name",
                    parent=self,
                ),
                createAction(
                    "&Edit Script",
                    self._editScript,
                    shortcut="Crtl+E",
                    tip="Edit a new script file",
                    parent=self,
                ),
                createAction(
                    "&Quit",
                    self.close,
                    shortcut=QKeySequence.StandardKey.Close,
                    tip="Quit the application",
                    parent=self,
                ),
            ]
        )

        edit.addActions(
            [
                createAction(
                    "Reset Zoom",
                    lambda: self.resetZoomLevel.emit(),
                    "Ctrl+R",
                    "Reset scene zoom level",
                    None,
                    self,
                )
            ]
        )

    def _new(self):
        path, file = FileIOControl().openFile("Background Images (*.png)")
        if path:
            child = self._mdiArea.createMdiChild()
            child.setWindowTitle("Untitled")
            child.setBackgroundImage(path)
            child.showMaximized()

    def _open(self):
        path, file = FileIOControl().openFile("Scene Files (*.txt)")
        if path:
            child = self._mdiArea.createMdiChild()
            child.setWindowTitle(file)
            child.deserialize(path)
            child.showMaximized()

    def _save(self):
        # grab the active document before opening the save file dialog
        document = self._mdiArea.activeSubWindow().widget()
        if not isinstance(document, SceneEditor):
            return

        path, file = FileIOControl().saveFile("Scene Files (*.txt)")
        if path:
            document.serialize(path)
            document.setWindowTitle(file)

    def _editScript(self):
        child = SceneEditor()
        self._mdiArea.addSubWindow(child)
        child.showMaximized()

    def closeEvent(self, e: QEvent):
        self._mdiArea.closeAllSubWindows()
        if self._mdiArea.currentSubWindow():
            e.ignore()
        else:
            SettingsManager().write(self)
            e.accept()
