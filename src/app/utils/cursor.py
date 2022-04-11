from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QPixmap
from functools import wraps, partial
import app.resources


""" Change the cursor used for a tool for the duration of the class instance """


def setCursor(cls=None, *, cursor: str, hotX: int = -1, hotY: int = -1):
    if not cls:
        return partial(setCursor, cursor=cursor, hotX=hotX, hotY=hotY)

    @wraps(cls)
    def wrapper(*args, **kwargs):
        class DecoratedTool:
            def __init__(self, *args, **kwargs):
                self.tool = cls(*args, **kwargs)

            def __getattr__(self, name):
                method = self.tool.__getattribute__(name)

                if method.__name__ == "enable":
                    self.tool._scene.views()[0].setCursor(
                        QCursor(QPixmap(cursor), hotX, hotY)
                    )
                    return method
                elif method.__name__ == "disable":
                    self.tool._scene.views()[0].setCursor(QCursor(Qt.ArrowCursor))
                    return method
                return method

        return DecoratedTool(*args, **kwargs)

    return wrapper