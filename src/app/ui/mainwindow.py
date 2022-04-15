from PyQt5.QtCore import Qt, QSize, QEvent, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import (
    QMainWindow,
    QMenuBar,
    QMenu,
    QAction,
    QDockWidget,
    QWidget,
    QToolBar,
    QListWidget,
)
from PyQt5.QtGui import QKeySequence, QMouseEvent
from app.utils.action import *
from app.utils.fileio import FileIOControl
from app.utils.settings import SettingsManager
from app.script.scripteditor import ScriptEditor
from app.scene.sceneeditor import SceneEditor
from .statusbar import StatusBar
from .mdicontainer import MdiContainer
from .filebrowser import FileBrowser
from .propertyeditor import PropertyEditor
from ..model.document import DocumentModel


class MainWindow(QMainWindow):

    resetZoomLevel = pyqtSignal()

    def __init__(self):
        super().__init__()

        self._doc: DocumentModel = None

        self._isZenModeActive = False

        self.setWindowTitle("Adventure Drive")
        self._setupUi()
        self.setStatusBar(StatusBar())
        SettingsManager().read(self)

    def _setupUi(self) -> None:
        self.setMinimumSize(QSize(800, 600))
        self._mdiArea = MdiContainer(self)
        self.setCentralWidget(self._mdiArea)

        self._createMenus()
        StatusBar().showMessage("Ready", 4000)

        self._property = PropertyEditor(self)
        self.addDockWidget(Qt.RightDockWidgetArea, self._property)

        # self._filebrowser = FileBrowser(self)
        # self.addDockWidget(Qt.LeftDockWidgetArea, self._filebrowser)

    #! TO DISABLE menu entries use action.setEnable(False)
    def _createMenus(self) -> None:
        menubar = self.menuBar()
        file = menubar.addMenu("&File")
        edit = menubar.addMenu("&Edit")
        view = menubar.addMenu("&View")

        zenmode = createAction(
            "&Zen Mode",
            self._zenmode,
            shortcut="Ctrl+Tab",
            tip="Enter Distraction Free Mode",
            parent=self,
        )

        # hiden menus don't trigger actions
        # so this action must be added to the mainwindow itself
        # to be able to leave zenmode
        self.addAction(zenmode)

        view.addActions(
            [
                zenmode,
                createAction(
                    "&Full Screen",
                    self._fullScreen,
                    shortcut="F11",
                    tip="Enter Full Screen Mode",
                    parent=self,
                ),
            ]
        )

        file.addActions(
            [
                createAction(
                    "&New",
                    lambda: self._new("scene"),
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

    def _zenmode(self) -> None:
        if self._isZenModeActive:
            self._property.show()
            self.setWindowState(Qt.WindowMaximized)
            self.menuBar().show()
            self.statusBar().show()

            self._isZenModeActive = False
        else:
            self._property.hide()
            self.setWindowState(Qt.WindowFullScreen)
            self.menuBar().hide()
            self.statusBar().hide()

            self._isZenModeActive = True

    def _fullScreen(self) -> None:
        if self.windowState() & Qt.WindowMaximized:
            self.setWindowState(Qt.WindowFullScreen)
        else:
            self.setWindowState(Qt.WindowMaximized)

    def _new(self, doctype: str) -> None:
        if doctype == "scene":
            filter_ = "Background Images (*.png)"
        elif doctype == "script":
            filter_ = "Script Files (*.txt)"

        path, file = FileIOControl().openFile(filter_)
        if path:
            child = self._mdiArea.createMdiChild(doctype)
            child.setWindowTitle("Untitled")

            if doctype == "scene":
                child.setBackgroundImage(path)
            child.showMaximized()

    def _open(self) -> None:
        path, file = FileIOControl().openFile("Scene Files (*.txt)")
        if path:
            self._doc = DocumentModel()
            self._doc.sigDocumentChanged.connect(self._property.sltSetModel)

            child: SceneEditor = self._mdiArea.createMdiChild("scene", self._doc)
            child.setWindowTitle(file)
            child.deserialize(path)
            child.showMaximized()

    def _save(self) -> None:
        # grab the active document before opening the save file dialog
        document = self._mdiArea.activeSubWindow().widget()
        if not isinstance(document, (SceneEditor, ScriptEditor)):
            return

        path, file = FileIOControl().saveFile("Scene Files (*.txt)")
        if path:
            document.serialize(path)
            document.setWindowTitle(file)

    def _editScript(self) -> None:
        child = self._mdiArea.createMdiChild("script")
        child.showMaximized()

    def closeEvent(self, e: QEvent) -> None:
        self._mdiArea.closeAllSubWindows()
        if self._mdiArea.currentSubWindow():
            e.ignore()
        else:
            SettingsManager().write(self)
            e.accept()
