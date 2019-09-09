import copy
import json
import pickle
import shutil
import threading

import numpy as np
from PyQt5.QtCore import Qt, pyqtSignal, QBasicTimer
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *

from core.ComboCheckBox import ComboCheckBox
from core.util import get_logger, get__function_name, get_all_json_data, read_ini, write_ini
from s3dis.opt_s3dis_gt import GT
from s3dis.opt_s3dis_gt import obj_2_json
from s3dis.opt_s3dis_gt import main
from s3dis.pc_widget import GLWidget
import copy
import os
from spellchecker import SpellChecker

spell = SpellChecker()


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
        print('progress_bar_animate')
        self.progress_bar.setValue(0)
        self.timer.start(100, self)

        if self.flag == 0:
            self.flag = 1
        else:
            self.progress_bar.setValue(100)
            self.statusBar().showMessage("successful")

            self.flag = 0

    def timerEvent(self, e):
        print(self.step)
        if self.step >= 50:
            self.timer.stop()
            self.window.change_mesh()
            self.progress_bar.setValue(100)
            self.statusBar().showMessage("loaded file:==>" + self.window.json_data_path)
        self.step += self.step + 1
        self.progress_bar.setValue(self.step)

    def wait_for_loading(self):
        self.progress_bar.setValue(self.progress_bar.value() + 100)


class Window(QWidget):
    signal = pyqtSignal(str)

    def __init__(self):
        super(Window, self).__init__()
        # widget init

        self.gl_widget = GLWidget(self)
        self.top_text_hint = QTextEdit()
        self.file_directory = QLineEdit('请输入3d数据目录')
        self.json_directory = QLineEdit('请输入json目录')
        self.lock_button = QPushButton('锁定')
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
        self.wait_progress_bar = QProgressDialog()
        self.clip_board = QApplication.clipboard()
        # init
        self.json_data_path = ''
        self.json_data = []
        self.operation_stack = []
        self.merged_label_checked = []
        self.json_path_new = ''
        self.label_new = ''
        self.dir_path = ''
        self.check_box_list = []
        self.check_label_index = []
        self.label_dict = {}
        self.json_directory_path = ''
        self.checkbox_layout_list = []
        self.merge_label_index = []
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        self.gl_widget.sizeHint()
        main_layout.addWidget(self.gl_widget, 4)

        # child layout

        self.child_layout_v_1 = QVBoxLayout()
        top_child_layout = QHBoxLayout()
        child_layout_h_0 = QHBoxLayout()
        child_layout_h_1 = QHBoxLayout()
        self.child_layout_h_2 = QHBoxLayout()
        child_layout_h_3 = QHBoxLayout()
        child_layout_h_4 = QHBoxLayout()
        '''
        top_child_layout
        '''
        if not os.path.exists(read_ini()):
            print(self.json_directory_path)
            self.file_directory.setClearButtonEnabled(True)
            self.file_directory.textChanged.connect(lambda: self.on_click(self.file_directory))
            self.json_directory.setClearButtonEnabled(True)
            self.json_directory.textChanged.connect(lambda: self.on_click(self.json_directory))
            self.lock_button.clicked.connect(lambda: self.on_click(self.lock_button))
            self.wait_progress_bar.reset()
        else:
            self.json_directory_path = read_ini()
            self.wait_progress_bar = None

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

        '''
        child_layout_h_3
        '''

        # merged label choose
        self.merged_label_box.show()
        self.merged_label_box.fn_init_data(self.json_data)
        self.merged_label_box.setMinimumContentsLength(15)
        self.merged_label_box.setStyle(QStyleFactory.create('Windows'))
        # self.merged_label_box.currentIndexChanged.connect(lambda: self.on_click(self.merged_label_box))
        self.merged_label_box.signal.connect(lambda: self.on_click(self.merged_label_box))
        # display combined group
        self.display_relations_list.currentItemChanged.connect(lambda: self.display_all_relations)
        # give a new label
        self.label_edit.textChanged.connect(lambda: self.on_click(self.label_edit))
        # merge the group
        self.merge_mesh_button.clicked.connect(lambda: self.on_click(self.merge_mesh_button))

        '''
        child_layout_h_4
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
        if not os.path.exists(read_ini()):
            top_child_layout.addWidget(self.file_directory)
            top_child_layout.addWidget(self.json_directory)
            top_child_layout.addWidget(self.lock_button)
        child_layout_h_0.addWidget(self.top_text_hint, 0, Qt.AlignCenter)
        child_layout_h_1.addWidget(self.choose_file, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_1.addWidget(self.display_mesh, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_1.addWidget(self.label_box, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_3.addWidget(self.merged_label_box, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_3.addWidget(self.label_edit, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_3.addWidget(self.merge_mesh_button, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_4.addWidget(self.cancel_button, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_4.addWidget(self.save_button, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_4.addWidget(self.review_button, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_4.addWidget(self.all_in_one, 0, Qt.AlignLeft | Qt.AlignTop)

        self.child_layout_v_1.addLayout(child_layout_h_0, 2)
        if not os.path.exists(read_ini()):
            self.child_layout_v_1.addLayout(top_child_layout, 1)
        self.child_layout_v_1.addLayout(child_layout_h_1, 1)
        self.child_layout_v_1.addLayout(child_layout_h_3, 1)
        self.child_layout_v_1.addLayout(child_layout_h_4, 1)

        self.child_layout_v_1.addStretch(4)
        main_layout.addLayout(self.child_layout_v_1)
        main_layout.addStretch(1)
        self.setLayout(main_layout)
        self.setWindowTitle("Label Tools")
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def compare_adjust_index(self, merge_index):
        for index in self.label_box.get_checked_box():
            if index not in merge_index:
                self.label_box.qCheckBox[index].setChecked(False)
        for index in merge_index:
            if index not in self.label_box.get_checked_box():
                self.label_box.qCheckBox[index].setChecked(True)

    def on_click(self, widget):
        if widget == self.merged_label_box:
            get_logger().info(get__function_name() + "-->")
            _list = self.merged_label_box.items
            get_logger().info(str(_list))
            index = self.check_label_index
            merge_index = self.merged_label_box.get_checked_box()
            index_pair = {}
            print(index)
            for i in merge_index:
                index_pair[i] = self.merge_label_index[i]
            print('fn_clear')
            if merge_index:
                print('---', merge_index)
                print('index_pair', [index_pair[x] for x in merge_index])
                selected_index = [index_pair[x] for x in merge_index]
                self.draw_labeled_mesh(selected_index)
                self.compare_adjust_index(selected_index)
        if widget == self.label_box:
            get_logger().info(get__function_name() + '-->')
            original_list = self.label_box.items
            get_logger().info(str(original_list))
            index = self.label_box.get_checked_box()
            get_logger().info(str(index))

            self.draw_labeled_mesh(index)
        if widget == self.display_mesh:
            index = self.label_box.get_checked_box()
            self.gl_widget.pointcloud.change_data()
            self.gl_widget.update()
        if widget == self.choose_file:
            if self.json_directory_path == '':
                self.error_message.setWindowTitle('illegal operation !')
                self.error_message.showMessage(
                    'json directory not chosen')
            directory = self.file_dialog.getOpenFileName(parent=self, caption='选取文件夹',
                                                         directory=self.json_directory_path,
                                                         filter='JSON files(*.json)')
            if directory[0] != self.json_data_path and directory[0] != '' and directory is not None:
                self.json_data_path = directory[0]
                self.signal.emit(directory[0])

        if widget == self.label_edit:
            self.label_new = self.label_edit.text()
        if widget == self.lock_button:
            # TODO 文件夹检查
            if self.json_directory_path != '' and os.path.exists(self.json_directory_path) and os.listdir(
                    self.json_directory_path):
                pass
            else:
                if self.file_directory != '' and os.path.exists(self.dir_path):
                    dir_path = self.file_directory.text()
                    file_count = len(os.listdir(dir_path))
                    self.wait_progress_bar.resize(340, self.wait_progress_bar.height())
                    self.wait_progress_bar.setWindowTitle("Json 文件生成中，请耐心等待！：）")
                    label = QLabel()
                    label.setWordWrap(True)
                    label.setMinimumHeight(17)
                    self.wait_progress_bar.setLabel(label)
                    self.wait_progress_bar.show()
                    self.wait_progress_bar.setValue(20)
                    self.wait_progress_bar.setValue(40)
                    self.wait_progress_bar.setValue(90)
                    main(dir_path, self.json_directory_path)
                    self.wait_progress_bar.setValue(100)
                    self.json_directory.setVisible(False)
                    self.file_directory.setVisible(False)
                    self.lock_button.setGraphicsEffect(QGraphicsBlurEffect())
                    write_ini(self.json_directory_path)
                else:
                    self.error_message.setWindowTitle('illegal operation !')
                    self.error_message.showMessage(
                        'please give a existed directory that contains the 3D data')
        if widget == self.file_directory:
            self.dir_path = self.file_directory.text()
        if widget == self.json_directory:
            self.json_directory_path = self.json_directory.text()
        if widget == self.merge_mesh_button:
            if self.label_new == '':
                self.error_message.setWindowTitle('illegal operation !')
                self.error_message.showMessage(
                    'please give a new label to complete the merge operation')
                self.merged_label_box.clear_checked_state()
            else:
                flag = True
                for tag in spell.unknown(self.label_new.split()):
                    self.error_message.setWindowTitle('illegal operation !')
                    self.error_message.showMessage('wrong label please correct it as--->' + spell.correction(tag))
                    self.label_edit.clear()
                    flag = False
                if flag:
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
                self.gl_widget.update()
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
        self.init_single_class_label()

    def add_check_box(self, i):
        check_box = QCheckBox()
        check_box.setCheckable(True)
        check_box.stateChanged.connect(lambda: self.on_check(check_box, i))
        self.check_box_list.append(check_box)

    def init_single_class_label(self):

        for child in self.check_box_list:
            print('---', child)
            child.setParent(None)
            for child_layout in self.checkbox_layout_list:
                child_layout.removeWidget(child)
                child_layout.setParent(None)
                self.child_layout_v_1.removeItem(child_layout)
        self.check_box_list = []
        self.label_dict = {}
        get_logger().info(get__function_name() + '-->' + self.json_data_path)
        label_list = self.gl_widget.pointcloud.label_list
        for i, label in enumerate(label_list):
            if label not in self.label_dict.keys():
                self.label_dict[label] = []
            self.label_dict[label].append(i)
        print(self.label_dict)
        for i in range(len(list(self.label_dict))):
            self.add_check_box(i)
        for i, (key, value) in enumerate(self.label_dict.items()):
            self.check_box_list[i].setText(key)
            print('---index', i)
        print(self.check_box_list)
        layout_count = len(self.check_box_list) % 5 + 1
        for i in range(layout_count + 1):
            self.checkbox_layout_list.append(QHBoxLayout())
        count = 0
        layout_index = 0
        for c in self.check_box_list:
            count += 1
            self.checkbox_layout_list[layout_index].addWidget(c, 0, Qt.AlignLeft | Qt.AlignTop)
            if count % 5 == 0 or count == len(self.check_box_list):
                self.child_layout_v_1.insertLayout(2, self.checkbox_layout_list[layout_index], 1)
                layout_index += 1

    def on_check(self, widget, index):
        print(index)
        self.check_label_index = []
        for i, check_box in enumerate(self.check_box_list):
            if check_box.isChecked():
                value_list = self.label_dict.values()
                label = list(self.label_dict.keys())[i]
                if 'group' in label:
                    print(self.label_edit.text())
                    if 'area' in self.label_edit.text():
                        new_label = self.label_edit.text()
                    else:
                        new_label = 'area'
                    if new_label != self.clip_board.text():
                        self.label_edit.clear()
                    self.clip_board.setText(new_label)
                    self.label_edit.setText(new_label)
                else:
                    new_label = list(self.label_dict.keys())[i] + ' group'
                    if new_label != self.clip_board.text():
                        self.label_edit.clear()
                    self.clip_board.setText(list(self.label_dict.keys())[i] + ' group')
                    self.label_edit.setText(new_label)
                self.check_label_index.extend(list(value_list)[i])
                sorted(set(self.check_label_index), key=self.check_label_index.index)
                print(self.check_label_index)
                print(self.label_dict)
        print(self.check_label_index)

        self.label_box.fn_clear()
        self.label_box.fn_set_checked(self.check_label_index)
        self.merged_label_box.clear()
        self.merged_label_box.fn_init_data([self.label_box.items[x] for x in self.label_box.get_checked_box()])
        self.merge_label_index = self.label_box.get_checked_box()
        self.draw_labeled_mesh(self.check_label_index)

    def change_mesh(self, path=''):
        if path == '':
            path = self.json_data_path
            self.gl_widget.change_data(path)
            self.json_data_path = path
            self.change_label()
            if os.path.exists(self.json_data_path.split('.')[0] + '.pickle'):
                self.deserialize_stack(self.json_data_path.split('.')[0] + '.pickle')
            else:
                self.operation_stack = []

    def fake_change_mesh(self, index):
        self.gl_widget.pointcloud.hier_data = self.json_data
        fake_list = []
        for i, x in enumerate(self.json_data):
            if x['parent'] == -1:
                fake_list.append(i)
        print('fake_list', fake_list)
        self.gl_widget.pointcloud.hier_display_index = fake_list
        self.gl_widget.pointcloud.change_data()
        self.gl_widget.update()
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
        self.merged_label_box.clear()
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
        self.serialize_stack(self.operation_stack)
        self.error_message.setWindowTitle('写入完成')
        self.error_message.showMessage(
            'complete!')

    def serialize_stack(self, stack):
        with open(self.json_path_new.split('.')[0] + '.pickle', 'wb')as fp:
            pickle.dump(stack, fp)

    def deserialize_stack(self, path):
        try:
            with open(path, 'rb')as fp:
                self.operation_stack = pickle.load(fp)
        except:
            os.remove(path)
            self.operation_stack = []


class EventDisable(QWidget):
    ignore = False

    def eventFilter(self, obj, event):
        if self.ignore:
            QWidget.eventFilter(self, obj, event)
        else:
            pass
