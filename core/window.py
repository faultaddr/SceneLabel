import numpy as np
from OpenGL.raw.GL.VERSION.GL_1_0 import glClear
from OpenGL.raw.GL.VERSION.GL_1_1 import GL_COLOR_BUFFER_BIT
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QComboBox, QFileDialog
from PyQt5.QtCore import Qt

from core import cube
from core.util import get_up_down_face_coords
from .glwidget import GLWidget


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.initUI()

    def initUI(self):
        self.glWidget = GLWidget(self)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.glWidget)
        child_layout = QHBoxLayout()
        child_layout.addWidget(QPushButton(str(1)), 0, Qt.AlignLeft | Qt.AlignTop)
        # get label list
        label_list = ['sofa', 'table', 'bed']
        self.label_box = QComboBox()
        self.label_box.addItems(label_list)
        child_layout.addWidget(self.label_box, 0, Qt.AlignLeft | Qt.AlignTop)
        main_layout.addLayout(child_layout, 0)
        self.label_box.currentIndexChanged.connect(lambda: self.on_click(self.label_box))
        self.file_dialog = QFileDialog()
        directory=self.file_dialog.getExistingDirectory(self, '选取所有scan 的主文件夹', './')
        print(directory)
        self.setLayout(main_layout)
        self.setWindowTitle("Label Tools")

    def on_click(self, box):
        if box == self.label_box:
            print(box.currentIndex())
            # 画出当前的 box
            self.draw_labeled_box(box.currentIndex())

    def draw_labeled_box(self, index):
        self.glWidget.repaint_with_data(index)
