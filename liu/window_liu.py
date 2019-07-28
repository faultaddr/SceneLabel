import json
import threading

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *

from core.ComboCheckBox import ComboCheckBox
from core.util import get_logger, get__function_name, get_label_info, get_all_json_data
from liu.mesh_widget import GLWidget


class Window(QWidget):
    lock = threading.RLock()

    def __init__(self):
        super(Window, self).__init__()
        # widget init
        self.gl_widget = GLWidget(self)
        self.top_text_hint = QTextEdit()
        self.path_text = QLineEdit()
        self.choose_file = QPushButton('选取文件')
        self.display_mesh = QPushButton('显示面片')
        self.file_dialog = QFileDialog()
        self.label_box = ComboCheckBox()
        self.merged_label_box = ComboCheckBox()
        self.display_relations_list = QListWidget()
        self.error_message = QErrorMessage()
        self.merge_mesh_button = QPushButton('合并面片')
        self.edit_text = QLineEdit()
        self.delete_mesh_button = QPushButton('删除面片')
        self.save_button = QPushButton('写入')
        self.cancel_button = QPushButton('撤销')
        self.review_button = QPushButton('检查')
        # init
        self.json_data_path = ''
        self.json_data = []
        self.operation_stack = []
        self.label_stack = []
        self.merged_label_checked = []
        self.json_path_new = ''
        self.label = ''
        self.default_directory = '/data/SceneLabel/liu/liu_json'
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
        # change default path
        self.path_text.setText(self.default_directory)
        self.path_text.textChanged.connect(lambda: self.on_click(self.path_text))
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
        self.display_relations_list.currentItemChanged.connect(lambda: self.display_all_relations())
        # edit the label

        self.edit_text.textChanged.connect(lambda: self.edit_label())
        # merge the group
        self.merge_mesh_button.clicked.connect(lambda: self.on_click(self.merge_mesh_button))

        # delete the group
        self.delete_mesh_button.clicked.connect(lambda: self.on_click(self.delete_mesh_button))
        '''
        child_layout_h_3
        '''
        # cancel the last operation
        self.cancel_button.clicked.connect(lambda: self.on_click(self.cancel_button))
        # write all the operation
        self.save_button.clicked.connect(lambda: self.on_click(self.save_button))
        # review  merged mesh
        self.review_button.clicked.connect(lambda: self.on_click(self.review_button))

        # layout setting

        child_layout_h_0.addWidget(self.top_text_hint, 0, Qt.AlignCenter)
        child_layout_h_1.addWidget(self.path_text, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_1.addWidget(self.choose_file, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_1.addWidget(self.display_mesh, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_1.addWidget(self.label_box, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_2.addWidget(self.merged_label_box, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_2.addWidget(self.edit_text, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_2.addWidget(self.merge_mesh_button, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_2.addWidget(self.delete_mesh_button, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_3.addWidget(self.cancel_button, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_3.addWidget(self.save_button, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_3.addWidget(self.review_button, 0, Qt.AlignLeft | Qt.AlignTop)

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
        if widget == self.path_text:
            self.default_directory = widget.text()
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
                                                         directory=self.default_directory)
            if directory != '':
                self.json_data_path = directory[0]
                self.change_mesh(directory[0])
        if widget == self.merge_mesh_button:
            index = self.label_box.get_checked_box()
            labeled_index = self.merged_label_box.get_checked_box()
            print(labeled_index)
            self.opt_merge(index, labeled_index)
        if widget == self.delete_mesh_button:
            index = self.label_box.get_checked_box()
            self.delete_mesh(index)
        if widget == self.cancel_button:
            self.operation_stack.pop(-1)
        if widget == self.save_button:
            self.change_json()
        if widget == self.review_button:
            self.change_mesh(self.json_path_new)

    def change_label(self):
        get_logger().info(get__function_name() + '-->' + self.json_data_path)
        label_list = get_label_info(self.json_data_path)
        self.label_box.clear()
        self.label_box.fn_init_data(label_list)

    def change_mesh(self, path):
        self.gl_widget.change_data(path)
        self.json_data_path = path
        self.setWindowTitle("Label Tools :->" + path)
        self.change_label()
        self.operation_stack = []

    def draw_labeled_mesh(self, index_list):
        self.gl_widget.repaint_with_data(index_list)

    def display_all_relations(self):
        self.display_relations_list.clear()
        for operation in self.operation_stack:
            self.display_relations_list.addItem(str(operation))

    def opt_merge(self, index, labeled_index):
        # TODO 1.build a buffer to store the operation
        # TODO 2.recursively change the parent of the under merged mesh to the new one
        # TODO 3.in the end write the new json format doc to represent ground truth
        # the first one in the operation_stack[i] is the target label
        if len(labeled_index) > 1 or len(labeled_index) == 0:
            self.error_message.setWindowTitle('illegal operation !')
            self.error_message.showMessage(
                'cannot do the merge because of the illegal operation\n only could set one label to merge into')
            self.merged_label_box.clear_checked_state()
        else:
            print('---merged label', labeled_index)
            first_index = index.pop(labeled_index[0])
            index.insert(0, first_index)
            self.operation_stack.append(index)
            self.label_stack.append(self.label)

    def delete_mesh(self, index):
        self.json_data = self.gl_widget.mesh.hier_data
        for i in index:
            self.json_data[i]['parent'] = '-2'
        model_array = get_all_json_data(self.json_data_path)
        self.json_path_new = self.json_data_path.split('.')[0].replace('_copy', '') + '_copy' + '.json'
        for i, model in enumerate(model_array):
            for data in self.json_data:
                if model['newModel'] == data['newModel']:
                    model_array[i] = data
                if model['parent'] == "0" and data['parent'] != str(model['newModel']):
                    model['children'].remove(str(data['newModel']))
        with open(self.json_path_new, 'w')as f:
            json.dump(model_array, f)
        get_logger().debug(get__function_name() + '-->' + 'json copy write complete')

    def change_json(self):
        # eater = EventDisable()
        # self.installEventFilter(eater)
        self.json_data = self.gl_widget.mesh.hier_data
        model_array = get_all_json_data(self.json_data_path)
        print(str(self.operation_stack))
        print('--->', self.json_data)
        for index, op in enumerate(self.operation_stack):
            print('0-1:', op[0], op[1])
            for i in op[1:]:
                self.json_data[i]['parent'] = str(self.json_data[op[0]]['newModel'])
                self.json_data[op[0]]['children'].append(str(self.json_data[i]['newModel']))
                self.json_data[op[0]]['leaf_group'].extend(self.json_data[i]['leaf_group'])
        if not self.label_stack and self.label != '':
            index = self.label_box.get_checked_box()
            for i in index:
                self.json_data[i]['label'] = self.label.split(' ')
        for i, model in enumerate(model_array):
            for data in self.json_data:
                if model['newModel'] == data['newModel']:
                    model_array[i] = data
                if model['parent'] == "0" and data['parent'] != str(model['newModel']):
                    model['children'].remove(str(data['newModel']))
        self.json_path_new = self.json_data_path.split('.')[0].replace('_copy', '') + '_copy' + '.json'
        with open(self.json_path_new, 'w')as f:
            json.dump(model_array, f)
        get_logger().debug(get__function_name() + '-->' + 'json copy write complete')
        self.label = ''
        self.operation_stack = []
        self.label_stack = []
        self.edit_text.clear()
        # eater.ignore = True

    def edit_label(self):

        self.label = self.edit_text.text()


class EventDisable(QWidget):
    ignore = False

    def eventFilter(self, obj, event):
        if self.ignore:
            QWidget.eventFilter(self, obj, event)
        else:
            pass
