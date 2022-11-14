from functools import partial, wraps

import app.resources
from app.tool.abstracttool import AbstractTool
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QPixmap


def setCursor(cls=None, *, cursor: str, hotX: int = -1, hotY: int = -1):
    """Decorator to change the mouse cursor used by a tool.
    When the tool is disabled the default cursor is restored.


    Args:
        cursor (str): path to the cursor in the qrc resource file
        cls (_type_, optional): Tool class. Defaults to None.
        hotX (int, optional): Cursor image hotspot x coordinate. Defaults to -1.
        hotY (int, optional): Cursor image hotspot y coordinate. Defaults to -1.

    Returns:
        _type_: The Decorated tool.
    """
    if not cls:
        return partial(setCursor, cursor=cursor, hotX=hotX, hotY=hotY)

    @wraps(cls)
    def wrapper(*args, **kwargs):
        class DecoratedTool:
            def __init__(self, *args, **kwargs):
                self.tool: AbstractTool = cls(*args, **kwargs)

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
