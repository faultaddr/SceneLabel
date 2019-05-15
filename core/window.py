from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QComboBox, QFileDialog, QStyleFactory, \
    QTextEdit, QCheckBox, QItemDelegate, QListWidget, QAbstractItemView, QListWidgetItem, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.uic.properties import QtCore, QtGui

from core.ComboCheckBox import ComboCheckBox
from core.glwidget import GLWidget as gl_widget

from PyQt5.QtWidgets import QComboBox, QLineEdit, QListWidget, QCheckBox, QListWidgetItem


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.data = []
        self.init_ui()

    def init_ui(self):
        self.gl_widget = gl_widget(self)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.gl_widget)
        child_layout = QHBoxLayout()
        self.choose_file = QPushButton('选取文件夹   ')
        child_layout.addWidget(self.choose_file, 0, Qt.AlignLeft | Qt.AlignTop)
        # get label list
        label_list = []

        self.label_box = ComboCheckBox()
        self.label_box.show()
        self.label_box.fn_init_data(self.data)
        self.label_box.setStyle(QStyleFactory.create('Windows'))
        self.label_box.currentIndexChanged.connect(lambda: self.on_click(self.label_box))
        self.label_box.setMinimumContentsLength(20)

        self.choose_file.toggle()
        # 点击信号与槽函数进行连接，这一步实现：在控制台输出被点击的按钮
        self.choose_file.clicked.connect(lambda: self.on_click(self.choose_file))
        child_layout.addWidget(self.label_box, 0, Qt.AlignLeft | Qt.AlignTop)
        self.file_dialog = QFileDialog()

        main_layout.addLayout(child_layout, 0)
        self.setLayout(main_layout)
        self.setWindowTitle("Label Tools")

    def on_click(self, widget):
        if widget == self.label_box:
            print(widget.currentIndex())
            # 画出当前的 box
            self.draw_labeled_box(widget.currentIndex())
        if widget == self.choose_file:
            directory = self.file_dialog.getExistingDirectory(self, '选取 文件夹', '')
            print(directory)
            self.change_obbs(directory)

    def draw_labeled_box(self, index):
        self.gl_widget.repaint_with_data(index)

    def change_obbs(self, path):

        self.gl_widget.change_data(path)
        self.data = self.gl_widget.get_label_data()
        print(self.data)
        self.label_box.clear()
        self.label_box.fn_init_data(self.data)
