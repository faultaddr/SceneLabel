from PyQt5.QtWidgets import QHBoxLayout, QWidget

from .glwidget import GLWidget


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.initUI()

    def initUI(self):
        self.glWidget = GLWidget(self)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.glWidget)
        self.setLayout(mainLayout)
        self.setWindowTitle("Simple GL")