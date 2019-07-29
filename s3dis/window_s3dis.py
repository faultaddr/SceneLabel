import copy
import json
import threading

import numpy as np
from PyQt5.QtCore import Qt, pyqtSignal, QBasicTimer
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *

from core.ComboCheckBox import ComboCheckBox
from core.util import get_logger, get__function_name, get_all_json_data
from s3dis.opt_s3dis_gt import GT
from s3dis.opt_s3dis_gt import obj_2_json
from s3dis.pc_widget import GLWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.progress_bar = QProgressBar(self)
        self.statusBar().showMessage('运行中...')
        self.setWindowTitle("Label Tools (for Beta Lab use only)")
        self.label_first = QLabel()
        self.label_second = QLabel()
        self.flag = 0
        self.window = Window()
        self.step = 0
        self.timer = QBasicTimer()
        self.init_ui()

    def init_ui(self):
        self.window.signal.connect(self.progress_bar_animate)

        self.setCentralWidget(self.window)

        self.statusBar().addPermanentWidget(self.label_first)
        self.statusBar().addPermanentWidget(self.label_second)
        self.statusBar().addPermanentWidget(self.progress_bar)
        # self.statusBar().addWidget(self.progressBar)

        # This is simply to show the bar
        self.progress_bar.setGeometry(0, 0, 100, 5)
        self.progress_bar.setRange(0, 100)  # 设置进度条的范围

    def progress_bar_animate(self):
        self.progress_bar.setValue(20)
        if self.flag == 0:
            self.flag = 1
        else:
            self.progress_bar.setValue(100)
            self.statusBar().showMessage("successful")

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
        self.step += self.step + 1
        self.progress_bar.setValue(self.step)

    def wait_for_loading(self):
        self.progress_bar.setValue(self.progress_bar.value() + 100)


class Window(QWidget):
    signal = pyqtSignal(int)

    def __init__(self):
        super(Window, self).__init__()
        # widget init
        self.gl_widget = GLWidget(self)
        self.top_text_hint = QTextEdit()
        self.display_mesh = QPushButton('显示点云')
        self.choose_file = QPushButton('选取文件')
        self.file_dialog = QFileDialog()
        self.label_box = ComboCheckBox()
        self.merged_label_box = ComboCheckBox()
        self.display_relations_list = QListWidget()
        self.error_message = QErrorMessage()
        self.label_edit = QLineEdit()
        self.merge_mesh_button = QPushButton('合并点云')
        self.save_button = QPushButton('写入')
        self.cancel_button = QPushButton('撤销')
        self.review_button = QPushButton('检查')
        self.all_in_one = QPushButton('一键写入')
        # init
        self.json_data_path = ''
        self.json_data = []
        self.operation_stack = []
        self.merged_label_checked = []
        self.json_path_new = ''
        self.label_new = ''
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        self.gl_widget.sizeHint()
        main_layout.addWidget(self.gl_widget, 4)

        # child layout

        child_layout_v_1 = QVBoxLayout()
        child_layout_h_0 = QHBoxLayout()
        child_layout_h_1 = QHBoxLayout()
        child_layout_h_2 = QHBoxLayout()
        child_layout_h_3 = QHBoxLayout()
        '''
        child_layout_h_0
        '''
        # text hint
        color = QColor()
        self.top_text_hint.setTextColor(color.fromRgb(255, 0, 0))
        self.top_text_hint.setAlignment(Qt.AlignCenter)
        self.top_text_hint.setPlainText(
            '请合并到只包含以下label \n sleep_area\n fireplace\n tv_group\n storage_area \n door_set\n rest_area\n desk_area')

        '''
        child_layout_h_1
        '''

        # display mesh
        self.display_mesh.toggle()
        self.display_mesh.clicked.connect(lambda: self.on_click(self.display_mesh))
        # choose file dialog
        self.choose_file.toggle()
        self.choose_file.clicked.connect(lambda: self.on_click(self.choose_file))
        # display label
        self.label_box.show()
        self.label_box.fn_init_data(self.json_data)
        self.label_box.setMinimumContentsLength(15)
        self.label_box.setStyle(QStyleFactory.create('Windows'))
        self.label_box.signal.connect(lambda: self.on_click(self.label_box))

        '''
        child_layout_h_2
        '''

        # merged label choose
        self.merged_label_box.show()
        self.merged_label_box.fn_init_data(self.json_data)
        self.merged_label_box.setMinimumContentsLength(15)
        self.merged_label_box.setStyle(QStyleFactory.create('Windows'))
        self.merged_label_box.currentIndexChanged.connect(lambda: self.on_click(self.merged_label_box))
        # display combined group
        self.display_relations_list.currentItemChanged.connect(lambda: self.display_all_relations)
        # give a new label
        self.label_edit.textChanged.connect(lambda: self.on_click(self.label_edit))
        # merge the group
        self.merge_mesh_button.clicked.connect(lambda: self.on_click(self.merge_mesh_button))

        '''
        child_layout_h_3
        '''
        # cancel the last operation
        self.cancel_button.clicked.connect(lambda: self.on_click(self.cancel_button))
        # write all the operation
        self.save_button.clicked.connect(lambda: self.on_click(self.save_button))
        # review  merged mesh
        self.review_button.clicked.connect(lambda: self.on_click(self.review_button))
        # all in on button (write & review)
        self.all_in_one.clicked.connect(lambda: self.on_click(self.all_in_one))

        # layout setting
        child_layout_h_0.addWidget(self.top_text_hint, 0, Qt.AlignCenter)
        child_layout_h_1.addWidget(self.choose_file, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_1.addWidget(self.display_mesh, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_1.addWidget(self.label_box, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_2.addWidget(self.merged_label_box, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_2.addWidget(self.label_edit, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_2.addWidget(self.merge_mesh_button, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_3.addWidget(self.cancel_button, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_3.addWidget(self.save_button, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_3.addWidget(self.review_button, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_3.addWidget(self.all_in_one, 0, Qt.AlignLeft | Qt.AlignTop)

        child_layout_v_1.addLayout(child_layout_h_0, 2)
        child_layout_v_1.addLayout(child_layout_h_1, 1)
        child_layout_v_1.addLayout(child_layout_h_2, 1)
        child_layout_v_1.addLayout(child_layout_h_3, 1)

        child_layout_v_1.addStretch(4)
        main_layout.addLayout(child_layout_v_1)
        main_layout.addStretch(1)
        self.setLayout(main_layout)
        self.setWindowTitle("Label Tools")
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_click(self, widget):
        if widget == self.label_box:
            get_logger().info(get__function_name() + '-->')
            original_list = self.label_box.items
            get_logger().info(str(original_list))
            index = self.label_box.get_checked_box()
            get_logger().info(str(index))
            self.merged_label_box.clear()
            self.merged_label_box.fn_init_data([original_list[x] for x in index])
            self.draw_labeled_mesh(index)
        if widget == self.display_mesh:
            index = self.label_box.get_checked_box()
            self.draw_labeled_mesh(index)
        if widget == self.choose_file:
            directory = self.file_dialog.getOpenFileName(parent=self, caption='选取文件夹',
                                                         directory='s3dis/s3dis_json')
            self.json_data_path = directory[0]
            self.change_mesh(directory[0])
        if widget == self.label_edit:
            self.label_new = self.label_edit.text()
        if widget == self.merge_mesh_button:
            if self.label_new == '':
                self.error_message.setWindowTitle('illegal operation !')
                self.error_message.showMessage(
                    'please give a new label to complete the merge operation')
                self.merged_label_box.clear_checked_state()
            else:
                index = self.label_box.get_checked_box()
                labeled_index = self.merged_label_box.get_checked_box()
                print(labeled_index)
                self.opt_merge(index, labeled_index)
        if widget == self.cancel_button:
            if self.operation_stack:
                index, json_data = self.operation_stack.pop(-1)
                self.json_data = json_data
                self.gl_widget.pointcloud.hier_data = self.json_data
                self.gl_widget.pointcloud.hier_display_index = np.arange(len(self.json_data)).tolist()
                self.gl_widget.pointcloud.change_data()
                self.change_label()
            else:
                pass

        if widget == self.save_button:
            self.write_json()
        if widget == self.review_button:
            pass
        if widget == self.all_in_one:
            # self.change_json()
            self.write_json()

    def change_label(self):
        get_logger().info(get__function_name() + '-->' + self.json_data_path)
        label_list = self.gl_widget.pointcloud.label_list
        self.label_box.clear()
        self.label_box.fn_init_data(label_list)

    def change_mesh(self, path):
        self.signal.emit(0)
        self.gl_widget.change_data(path)
        self.json_data_path = path
        self.change_label()
        self.operation_stack = []
        self.signal.emit(1)

    def fake_change_mesh(self, index):
        self.gl_widget.pointcloud.hier_data = self.json_data
        fake_list = []
        for i, x in enumerate(self.json_data):
            if x['parent'] == -1:
                fake_list.append(i)
        print('fake_list', fake_list)
        self.gl_widget.pointcloud.hier_display_index = fake_list
        self.gl_widget.pointcloud.change_data()
        self.change_label()

    def draw_labeled_mesh(self, index_list):
        self.gl_widget.repaint_with_data(index_list)

    def display_all_relations(self):
        self.display_relations_list.clear()
        for operation in self.operation_stack:
            self.display_relations_list.addItem(str(operation))

    def opt_merge(self, index, labeled_index):
        self.json_data = self.gl_widget.pointcloud.hier_data
        self.operation_stack.append((index, copy.deepcopy(self.json_data)))
        self.change_json()

    def change_json(self):
        self.json_data = self.gl_widget.pointcloud.hier_data
        model_array = get_all_json_data(self.json_data_path)
        if self.operation_stack:
            op = self.operation_stack[-1][0]
            gt = GT()
            gt.label = self.label_new
            gt.id = self.json_data[-1]['id'] + 1
            gt.children = []
            gt.parent = -1
            gt.path = []
            pair = []
            for i, d in enumerate(self.json_data):
                if d['parent'] == -1:
                    pair.append(i)
            print(pair)
            for j in op:
                self.json_data[pair[j]]['parent'] = gt.id
                gt.children.append(self.json_data[pair[j]]['id'])
                gt.path.extend(self.json_data[pair[j]]['path'])

            self.json_data.append(obj_2_json(gt))
            self.fake_change_mesh(pair)

    def write_json(self):
        self.json_path_new = self.json_data_path.split('.')[0].replace('_copy', '') + '_copy' + '.json'
        with open(self.json_path_new, 'w')as f:
            json.dump(self.json_data, f)
        get_logger().debug(get__function_name() + '-->' + 'json copy write complete')


class EventDisable(QWidget):
    ignore = False

    def eventFilter(self, obj, event):
        if self.ignore:
            QWidget.eventFilter(self, obj, event)
        else:
            pass
