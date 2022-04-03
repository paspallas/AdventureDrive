from PyQt5.QtPrintSupport import *
from PyQt5.Qsci import *
from PyQt5.QtGui import QFont, QColor, QKeySequence, QFontMetrics
from PyQt5.QtCore import Qt, QSize, QFileInfo, QEvent
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenuBar,
    QMenu,
    QAction,
    QWidget,
    QFileDialog,
    QMessageBox,
    QFrame,
    QVBoxLayout,
)

# TODO wrap into try block
from .lexer import AddLexer

WIDGET_TITLE = "Adventure Drive Script Editor"


class ScriptEditor(QsciScintilla):
    def __init__(self):
        super().__init__()

        self._is_doc_saved = False
        self._doc_path = None

        self._setupUi()
        self._configureEditor()
        # self._createMenus()
        self._make_connections()

    def _setupUi(self):
        self._setDocumentName("Untitled")

        # set the default font
        self._font = QFont("Fira Code")
        # self._font.setFamily("Courier")
        self._font.setFixedPitch(True)
        self._font.setPointSize(10)

        self._margin_font = QFont("Fira Code")
        self._margin_font.setFixedPitch(True)
        self._margin_font.setPointSize(9)

        self._lexer = AddLexer(self)
        self.setLexer(self._lexer)
        self._api = QsciAPIs(self._lexer)

        autocompletions = [
            "test_autocompletion",
            "somefunc(void 1, void 2)",
            "another func()",
        ]

        for ac in autocompletions:
            self._api.add(ac)
        self._api.prepare()

        self._lexer.setDefaultFont(self._font)

    def _setDocumentName(self, filename: str) -> None:
        self._doc_name = filename

        # visual cue for unsaved changes
        cue = "" if self._is_doc_saved else "*"

        self.setWindowTitle(f"{cue}{self._doc_name} - Script Editor")

    def _configureEditor(self):
        self.setUtf8(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setWrapMode(QsciScintilla.WrapWhitespace)
        self.setEolMode(QsciScintilla.EolUnix)
        self.setIndentationsUseTabs(False)
        self.setTabWidth(4)
        self.setTabIndents(False)
        self.setBackspaceUnindents(True)
        self.setIndentationGuides(True)
        self.setCaretLineVisible(True)
        self.setCaretWidth(1)
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.setMatchedBraceForegroundColor(QColor("#ff00ff89"))
        self.setAcceptDrops(False)

        # margins
        self.setMarginType(0, QsciScintilla.NumberMargin)
        fontmetrics = QFontMetrics(self._font)
        self.setMarginWidth(0, fontmetrics.width("00000") + 6)
        self.setMarginsFont(self._margin_font)

        # make last line scrollable to the top
        self.SendScintilla(QsciScintilla.SCI_SETENDATLASTLINE, False)

        # enable multiple-cursors editing
        self.SendScintilla(QsciScintilla.SCI_SETMULTIPLESELECTION, True)
        self.SendScintilla(QsciScintilla.SCI_SETMULTIPLESELECTION, True)
        self.SendScintilla(QsciScintilla.SCI_SETADDITIONALSELECTIONTYPING, True)

        # autocompletions
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.setAutoCompletionCaseSensitivity(False)

        # folding
        self.setFolding(QsciScintilla.BoxedTreeFoldStyle)

        # color styles
        self.setCaretForegroundColor(QColor("#fff2be00"))
        self.setCaretLineBackgroundColor(QColor("#ff101119"))
        self.setMarginsBackgroundColor(QColor("#ff161821"))
        self.setMarginsForegroundColor(QColor("#ff4a5672"))
        self.setFoldMarginColors(QColor("#ff161821"), QColor("#ff161821"))
        self.setSelectionBackgroundColor(QColor("#ff1c1d32"))

    def _createMenus(self):
        menubar = self.menuBar()

        filemenu = menubar.addMenu("&File")
        editmenu = menubar.addMenu("&Edit")

        openAction = QAction("&Open", self)
        openAction.setShortcut(QKeySequence.Open)
        openAction.triggered.connect(self._openfile)

        saveAction = QAction("&Save", self)
        saveAction.setShortcut(QKeySequence.Save)
        saveAction.triggered.connect(self._savefile)

        saveAsAction = QAction("&Save As", self)
        saveAsAction.setShortcut("Ctrl+Shift+S")
        saveAsAction.triggered.connect(lambda: self._savefile(saveas=True))

        undoAllAction = QAction("&Undo All", self)
        undoAllAction.setShortcut("Ctrl+Shift+U")
        undoAllAction.triggered.connect(self._undoAll)

        redoAllAction = QAction("&Redo All", self)
        redoAllAction.setShortcut("Ctrl+Shift+R")
        redoAllAction.triggered.connect(self._redoAll)

        filemenu.addAction(openAction)
        filemenu.addAction(saveAction)
        filemenu.addAction(saveAsAction)

        editmenu.addAction(undoAllAction)
        editmenu.addAction(redoAllAction)

    def _undoAll(self):
        """repeat undo until theres nothing left to undo"""
        while self.isUndoAvailable() == True:
            self.undo()

    def _redoAll(self):
        """repeat redo until theres nothing left to redo"""
        while self.isRedoAvailable() == True:
            self.redo()

    def _openfile(self) -> None:
        self._doc_path, _ = QFileDialog.getOpenFileName(
            None,
            "Open Script File",
            "./",
            filter="Adventure Drive Script Files (*.ads)",
        )
        if self._doc_path:
            self._is_doc_saved = True
            self._setDocumentName(QFileInfo(self._doc_path).fileName())
            with open(self._doc_path, "r", encoding="utf-8") as f:
                self.setText("".join(f.readlines()))

    def _savefile(self, saveas=False) -> None:
        if self._doc_path and saveas is False:
            self._is_doc_saved = True
            self._setDocumentName(QFileInfo(self._doc_path).fileName())
            self._save()
            return

        self._doc_path, _ = QFileDialog.getSaveFileName(
            None,
            "Save Script File",
            "./",
            filter="Adventure Drive Script Files (*.ads)",
        )
        if self._doc_path:
            self._is_doc_saved = True
            self._setDocumentName(QFileInfo(self._doc_path).fileName())
            self._save()

    def _save(self) -> None:
        with open(self._doc_path, "w", encoding="utf-8") as f:
            f.write(self.text())

    def closeEvent(self, e: QEvent):
        e.accept()
        return

        if self._is_doc_saved:
            e.accept()
        else:
            answer = QMessageBox.question(
                self,
                "Unsaved Changes",
                "You have unsaved changes, save before closing?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
            )
            if answer & QMessageBox.Save:
                self._savefile()
            elif answer & QMessageBox.Cancel:
                e.ignore()

    def set_fold(self, prev, line, fold, full):
        if prev[0] >= 0:
            fmax = max(fold, prev[1])
            for iter in range(prev[0], line + 1):
                self.SendScintilla(
                    QsciScintilla.SCI_SETFOLDLEVEL,
                    iter,
                    fmax | (0, QsciScintilla.SC_FOLDLEVELHEADERFLAG)[iter + 1 < full],
                )

    def line_empty(self, line):
        return self.SendScintilla(
            QsciScintilla.SCI_GETLINEENDPOSITION, line
        ) <= self.SendScintilla(QsciScintilla.SCI_GETLINEINDENTPOSITION, line)

    def modify(
        self,
        position,
        modificationType,
        text,
        length,
        linesAdded,
        line,
        foldLevelNow,
        foldLevelPrev,
        token,
        annotationLinesAdded,
    ):
        full = QsciScintilla.SC_MOD_INSERTTEXT | QsciScintilla.SC_MOD_DELETETEXT
        if ~modificationType & full == full:
            return
        prev = [-1, 0]
        full = self.SendScintilla(QsciScintilla.SCI_GETLINECOUNT)
        lbgn = self.SendScintilla(QsciScintilla.SCI_LINEFROMPOSITION, position)
        lend = self.SendScintilla(QsciScintilla.SCI_LINEFROMPOSITION, position + length)
        for iter in range(max(lbgn - 1, 0), -1, -1):
            if (iter == 0) or not self.line_empty(iter):
                lbgn = iter
                break
        for iter in range(min(lend + 1, full), full + 1):
            if (iter == full) or not self.line_empty(iter):
                lend = min(iter + 1, full)
                break
        for iter in range(lbgn, lend):
            if self.line_empty(iter):
                if prev[0] == -1:
                    prev[0] = iter
            else:
                fold = self.SendScintilla(QsciScintilla.SCI_GETLINEINDENTATION, iter)
                fold //= self.SendScintilla(QsciScintilla.SCI_GETTABWIDTH)
                self.set_fold(prev, iter - 1, fold, full)
                self.set_fold([iter, fold], iter, fold, full)
                prev = [-1, fold]
        self.set_fold(prev, lend - 1, 0, full)

    def _document_changed(self):
        self._is_doc_saved = False
        self._setDocumentName(self._doc_name)

    def _update_line_col(self):
        line, col = self.getCursorPosition()
        # self.statusBar().showMessage(f"Line. {line + 1}, Col. {col + 1}")

    def _make_connections(self):
        self.textChanged.connect(self._document_changed)
        self.SCN_MODIFIED.connect(self.modify)
        self.cursorPositionChanged.connect(self._update_line_col)
