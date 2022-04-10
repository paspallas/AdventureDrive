from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QFileInfo


class FileIOControl(QFileDialog):
    def __init__(self):
        super().__init__()

        self.path = None
        self.filename = None
        self.options = self.Options()
        self.options |= self.DontUseNativeDialog

    def openFile(self, fileFilter: str) -> (str, str):
        self.path, _ = self.getOpenFileName(
            self, "Open File", "", filter=fileFilter, options=self.options
        )

        if self.path and len(self.path) > 0:
            self._setFileName()
            return self.path, self.filename

        return None, None

    def saveFile(self, fileFilter: str) -> (str, str):
        self.path, _ = self.getSaveFileName(
            self, "Save File", "", filter=fileFilter, options=self.options
        )

        if self.path and len(self.path) > 0:
            self._setFileName()
            return self.path, self.filename

        return None, None

    def _setFileName(self):
        self.filename = QFileInfo(self.path).fileName()
