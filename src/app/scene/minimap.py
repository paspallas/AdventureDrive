from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QGraphicsRectItem


class MiniMap(QGraphicsView):
    def __init__(self, scene: QGraphicsScene = None, parent: QWidget = None):
        super().__init__(scene, parent)
