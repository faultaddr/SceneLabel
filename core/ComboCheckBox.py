from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QComboBox, QLineEdit, QListWidget, QCheckBox, QListWidgetItem

from core.util import get_logger, get__function_name


class ComboCheckBox(QComboBox):
    signal = pyqtSignal(int)

    def __init__(self, parent=None):
        super(ComboCheckBox, self).__init__(parent)
        self.fn_init_data(["请选择", "1", "2", "3", "4"])
        self.fn_init_event()
        self.checked_index = []

    def fn_init_data(self, list_items, text="请选择"):

        # self.setGeometry(QtCore.QRect(930, 50, 281, 31))
        # self.setStyleSheet("font: 16pt \"Agency FB\";")

        self.items = list_items
        self.row_num = len(self.items)
        self.selected_row_num = 0
        self.qCheckBox = []
        self.qLineEdit = QLineEdit()
        self.qLineEdit.setReadOnly(True)
        self.qListWidget = QListWidget()

        for i in range(0, self.row_num):
            self.addQCheckBox(i)
            self.qCheckBox[i].setChecked(False)

        self.list_selected_item = []

        self.setModel(self.qListWidget.model())
        self.setView(self.qListWidget)
        self.setLineEdit(self.qLineEdit)
        self.qLineEdit.setText(text)

    def get_checked_box(self):
        checked_index = []
        for i, box in enumerate(self.qCheckBox):
            if box.isChecked():
                checked_index.append(i)
        self.checked_index = checked_index
        return checked_index

    def clear_checked_state(self):
        for i, box in enumerate(self.qCheckBox):
            if box.isChecked():
                box.setCheckState(0)

    def listen_checkbox_sate(self, widget, index):
        get_logger().info(get__function_name() + '-->' + str(index))
        self.signal.emit(index)
        return index

    def fn_init_table(self):
        self.setGeometry(QtCore.QRect(930, 50, 281, 31))
        self.setStyleSheet("font: 16pt \"Agency FB\";")
        self.qLineEdit = QLineEdit()
        self.qLineEdit.setReadOnly(True)
        self.setLineEdit(self.qLineEdit)
        self.qLineEdit.setText("请选择")

    def fn_init_event(self):
        self.qCheckBox[0].stateChanged.connect(self.fn_check_all)
        for i in range(1, self.row_num):
            self.qCheckBox[i].stateChanged.connect(self.fn_check_multi_single)

    def addQCheckBox(self, i):
        qc = QCheckBox()
        qc.stateChanged.connect(lambda: self.listen_checkbox_sate(qc, i))
        self.qCheckBox.append(qc)
        qItem = QListWidgetItem(self.qListWidget)
        self.qCheckBox[i].setText(self.items[i])
        self.qListWidget.setItemWidget(qItem, self.qCheckBox[i])

    def fn_check_multi_single(self):
        show = ''
        Outputlist = []
        for i in range(1, self.row_num):
            if self.qCheckBox[i].isChecked() == True:
                Outputlist.append(self.qCheckBox[i].text())
        self.selected_row_num = len(Outputlist)
        self.list_selected_item = Outputlist
        # print(Outputlist)

        self.qLineEdit.setReadOnly(False)
        self.qLineEdit.clear()
        for i in Outputlist:
            show += i + ';'
        if self.selected_row_num == 0:
            self.qCheckBox[0].setCheckState(0)
            show = '请选择'
        elif self.selected_row_num == self.row_num - 1:
            self.qCheckBox[0].setCheckState(2)
            show = '全选'
        else:
            self.qCheckBox[0].setCheckState(1)
        self.qLineEdit.setText(show)
        self.qLineEdit.setReadOnly(True)

    def fn_check_all(self, status):
        if status == 2:  # 全选
            for i in range(1, self.row_num):
                self.qCheckBox[i].setChecked(True)
        elif status == 1:  # 不全选
            if self.selected_row_num == 0:
                self.qCheckBox[0].setCheckState(2)
        elif status == 0:  # 全不选
            self.fn_clear()

    def fn_clear(self):
        for i in range(self.row_num):
            self.qCheckBox[i].setChecked(False)

    def fn_set_checked(self, index_list):
        for index in index_list:
            self.qCheckBox[index].setChecked(True)
