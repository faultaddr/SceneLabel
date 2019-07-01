import os

from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QComboBox, QFileDialog, QStyleFactory, \
    QTextEdit, QCheckBox, QItemDelegate, QListWidget, QAbstractItemView, QListWidgetItem, QLineEdit, QVBoxLayout, \
    QDesktopWidget
from PyQt5.QtCore import Qt
from PyQt5.uic.properties import QtCore, QtGui

from core.ComboCheckBox import ComboCheckBox
from core.glwidget import GLWidget as gl_widget

from PyQt5.QtWidgets import QComboBox, QLineEdit, QListWidget, QCheckBox, QListWidgetItem


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.gl_widget = gl_widget(self)

    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.gl_widget)

    def init_data(self):
