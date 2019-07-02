import os

from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QComboBox, QFileDialog, QStyleFactory, \
    QTextEdit, QCheckBox, QItemDelegate, QListWidget, QAbstractItemView, QListWidgetItem, QLineEdit, QVBoxLayout, \
    QDesktopWidget
from PyQt5.QtCore import Qt
from PyQt5.uic.properties import QtCore, QtGui

from core.ComboCheckBox import ComboCheckBox
from liu.mesh_widget import GLWidget
from core.util import *
from PyQt5.QtWidgets import QComboBox, QLineEdit, QListWidget, QCheckBox, QListWidgetItem


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.json_data_path = ''
        self.json_data = []
        self.gl_widget = GLWidget(self)

        self.display_mesh = QPushButton('显示面片')
        self.choose_file = QPushButton('选取文件')
        self.file_dialog = QFileDialog()

        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.gl_widget)

        # child layout
        child_layout_v_1 = QVBoxLayout()
        child_layout_h_1 = QHBoxLayout()
        # 显示 面片
        self.display_mesh.toggle()
        self.display_mesh.clicked.connect(lambda: self.on_click(self.display_mesh))
        # choose file dialog
        self.choose_file.toggle()
        self.choose_file.clicked.connect(lambda: self.on_click(self.choose_file))

        child_layout_h_1.addWidget(self.choose_file, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_1.addWidget(self.display_mesh, 0, Qt.AlignLeft | Qt.AlignTop)

        child_layout_v_1.addLayout(child_layout_h_1, 1)
        main_layout.addLayout(child_layout_v_1, 0)
        self.setLayout(main_layout)
        self.setWindowTitle("Label Tools")
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_click(self, widget):
        if widget == self.display_mesh:
            self.draw_all_mesh()
        if widget == self.choose_file:
            directory = self.file_dialog.getOpenFileName(self, '选取文件夹')
            print(directory[0])
            self.json_data_path = directory[0]
            self.change_mesh(directory[0])

    def change_mesh(self, path):
        self.gl_widget.change_data(path)
        # 获取label信息以进行合并操作
        # self.json_data = get_json_data(path)

    def draw_all_mesh(self):
        self.gl_widget.repaint_with_data(self.data)
