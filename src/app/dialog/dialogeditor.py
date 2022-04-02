from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPlainTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QListWidget,
    QPushButton,
    QMenu,
    QMenuBar,
    QAction,
    QFileDialog,
    QStatusBar,
)
from PyQt5.QtCore import QSize, QModelIndex, QFileInfo
from PyQt5.QtGui import QKeySequence


class DialogEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        # currently opened file path
        self.path = None

        self._setupUI()
        self._setup_menu()
        self._make_connections()

    def _setupUI(self):
        self.setMinimumSize(QSize(800, 600))
        self.setWindowTitle("Dialog Editor")

        frame = QFrame(self)
        self.setCentralWidget(frame)
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        frame.setLayout(vbox)

        self._btn_save = QPushButton("Save", self)
        self._btn_add = QPushButton("Add", self)
        self._dialog_list = QListWidget(self)
        self._text_edit = QPlainTextEdit(self)

        hbox.addWidget(self._btn_add)
        hbox.addWidget(self._btn_save)
        hbox.insertStretch(0, 1)

        vbox.addWidget(self._text_edit)
        vbox.addLayout(hbox)
        vbox.addWidget(self._dialog_list)

        self.statusBar()

    def _setup_menu(self):
        menu_bar = self.menuBar()

        file = menu_bar.addMenu("&File")
        act_open = QAction("&Open", self)
        act_open.setShortcut(QKeySequence.Open)
        act_open.triggered.connect(self.file_open)
        act_save = QAction("&Save", self)
        act_save.setShortcut(QKeySequence.Save)
        act_save.triggered.connect(self.file_save)

        file.addActions([act_open, act_save])

    def _make_connections(self):
        self._dialog_list.clicked.connect(self._dialog_clicked)
        self._btn_save.clicked.connect(self._update_dialog)
        self._btn_add.clicked.connect(self._add_dialog)

    def _load_dialog_lines(self, text: list[str]) -> None:
        # Clean up previous state
        self._text_edit.clear()
        self._dialog_list.clear()

        for i, line in enumerate(text):
            if len(line) > 0:
                self._dialog_list.insertItem(i, line)

    def _dialog_clicked(self, qmodelindex: QModelIndex) -> None:
        item = self._dialog_list.currentItem()
        self._text_edit.clear()
        self._text_edit.insertPlainText(item.text())

    def _update_dialog(self) -> None:
        self._dialog_list.currentItem().setText(self._text_edit.toPlainText())

    def _add_dialog(self) -> None:
        index = self._dialog_list.count()
        text = self._text_edit.toPlainText()

        if len(text) > 0:
            item = self._dialog_list.insertItem(index, text)
            self._dialog_list.setCurrentItem(item)

    def file_open(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, caption="Open text file", directory="./", filter="Text files (*.txt)"
        )
        try:
            with open(path, "r", encoding="utf-8") as f:
                self._load_dialog_lines(f.read().split("\n"))

        except Exception as e:
            pass

        else:
            self.path = path

    def file_save(self) -> None:
        if self.path is None:
            self.file_save_as()

        try:
            with open(self.path, "w", encoding="utf-8") as f:
                count = self._dialog_list.count()
                for i in range(0, count):
                    sep = "\n" if i < count - 1 else ""
                    f.write(f"{self._dialog_list.item(i).text().strip():s}{sep}")

            self.statusBar().showMessage("File Saved!", 4000)

        except Exception as e:
            pass

    def file_save_as(self) -> None:
        self.path, _ = QFileDialog.getSaveFileName(
            self, caption="Save text file", directory="./", filter="Text files (*.txt)"
        )


if __name__ == "__main__":
    import sys

    app = QApplication([])
    editor = DialogEditor()
    editor.show()

    sys.exit(app.exec())
