from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QKeySequence, QIcon
from PyQt5.QtCore import QObject
from typing import Union, Optional


def createAction(
    name: str,
    callback: callable,
    shortcut: Union[QKeySequence, str] = None,
    tip: str = None,
    iconPath: str = None,
    parent: Optional[QObject] = None,
) -> QAction:

    """Helper method for creating QActions.

    Args:
        name (str): name that will be shown in the menu.
        callback (callable): on action triggered callback.
        shortcut ([QKeySequence, str] optional): keyboard shortcut. Defaults to None.
        tip (str, optional): status bar message tip. Defaults to None.
        iconPath (str, optional): path to an icon. Defaults to None.
        parent (QObject, optional): parent widget.
            It's recomended to set the window as parent of the action. Defaults to None.

    Returns:
        QAction: The action
    """

    if iconPath is not None:
        action = QAction(QIcon(iconPath), name, parent)
    else:
        action = QAction(name, parent)

    if shortcut is not None:
        action.setShortcut(shortcut)

    if tip is not None:
        action.setStatusTip(tip)

    if callback is not None:
        action.triggered.connect(callback)

    return action
