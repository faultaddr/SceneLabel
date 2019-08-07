import copy
import json

import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *

from core.ComboCheckBox import ComboCheckBox
from viewer.pc_widget import GLWidget


class Window(QWidget):
    path = ''
    obb_path = ''

    def __init__(self, path, obb_path):
        super(Window, self).__init__()
        # widget init
        self.gl_widget = GLWidget(self)
        self.path = path
        self.obb_path = obb_path
        # init
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        self.gl_widget.sizeHint()
        main_layout.addWidget(self.gl_widget, 4)

        self.setLayout(main_layout)
        self.setWindowTitle("Label Tools")
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.init_data()

    def init_data(self):
        self.gl_widget.change_data(self.path, self.obb_path)
