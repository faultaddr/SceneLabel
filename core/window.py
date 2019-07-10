import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QListWidget
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QFileDialog, QStyleFactory, \
    QVBoxLayout, \
    QDesktopWidget

from core.ComboCheckBox import ComboCheckBox
from core.glwidget import GLWidget as gl_widget


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.display_point = QPushButton('显示点云')
        self.display_relations_list = QListWidget()
        self.save_relation = QPushButton('保存当前关系')
        self.clear_write_btn = QPushButton('删除所有关系')
        self.revert_last_state = QPushButton('撤销当前写入')
        self.choose_write_directory = QFileDialog()
        self.gl_widget = gl_widget(self)
        self.write_btn = QPushButton('写入当前关系')
        self.relation_text = QComboBox()
        self.display_btn = QPushButton('显示组合obb')
        self.choose_file = QPushButton('选取文件夹   ')
        self.label_box = ComboCheckBox()
        self.file_dialog = QFileDialog()
        self.file_dialog_write = QFileDialog()
        self.data = []
        self.fake_data = []
        self.use_fake = False
        self.init_ui()
        self.obbs_path = ''
        self.save_path = ''
        self.relation_stack = []
        self.display_all_relations()

    def init_ui(self):

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.gl_widget)
        child_layout_h_1 = QHBoxLayout()
        child_layout_h_2 = QHBoxLayout()
        child_layout_h_3 = QHBoxLayout()
        child_layout_v_1 = QVBoxLayout()

        # label choose
        self.label_box.show()
        self.label_box.fn_init_data(self.data)
        self.label_box.setMinimumContentsLength(15)
        self.label_box.setStyle(QStyleFactory.create('Windows'))
        self.label_box.currentIndexChanged.connect(lambda: self.on_click(self.label_box))

        # choose file dialog
        self.choose_file.toggle()
        self.choose_file.clicked.connect(lambda: self.on_click(self.choose_file))

        # display combined relations
        self.display_btn.toggle()
        self.display_btn.clicked.connect(lambda: self.on_click(self.display_btn))

        # 关系选择
        self.relation_text.addItems(['0: 邻接', '1:支撑', '2:环绕', '3:并列'])
        self.relation_text.currentIndexChanged.connect(lambda: self.on_click(self.relation_text))

        # 保存关系
        self.save_relation.toggle()
        self.save_relation.clicked.connect(lambda: self.on_click(self.save_relation))
        # 写入到txt
        self.write_btn.toggle()
        self.write_btn.clicked.connect(lambda: self.on_click(self.write_btn))
        # 删除当前所有关系
        self.clear_write_btn.toggle()
        self.clear_write_btn.clicked.connect(lambda: self.on_click(self.clear_write_btn))
        # 撤销前一个写入的关系
        self.revert_last_state.toggle()
        self.revert_last_state.clicked.connect(lambda: self.on_click(self.revert_last_state))
        # 显示所有关系
        self.display_relations_list.clicked.connect(lambda: self.on_click(self.display_relations_list))
        self.display_relations_list.currentItemChanged.connect(lambda: self.display_all_relations())
        # 显示点云
        self.display_point.toggle()
        self.display_point.clicked.connect(lambda: self.on_click(self.display_point))

        child_layout_h_1.addWidget(self.choose_file, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_1.addWidget(self.label_box, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_1.addWidget(self.display_btn, 0, Qt.AlignLeft | Qt.AlignTop)

        child_layout_h_2.addWidget(self.display_relations_list, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_2.addWidget(self.display_point, 0, Qt.AlignLeft | Qt.AlignTop)

        child_layout_h_3.addWidget(self.relation_text, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_3.addWidget(self.save_relation, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_3.addWidget(self.write_btn, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_3.addWidget(self.revert_last_state, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_3.addWidget(self.clear_write_btn, 0, Qt.AlignLeft | Qt.AlignTop)

        child_layout_v_1.addLayout(child_layout_h_1, 1)
        child_layout_v_1.addLayout(child_layout_h_2, 1)
        child_layout_v_1.addLayout(child_layout_h_3, 1)
        main_layout.addLayout(child_layout_v_1, 0)
        self.setLayout(main_layout)
        self.setWindowTitle("Label Tools")
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def draw_multi_obb(self, index=None):
        if index:
            print('---draw_multi_obb', index)
            self.draw_labeled_box(index[0])
        else:
            checked_box = self.label_box.get_checked_box()
            print(checked_box)
            multi = []
            for j, checked_index in enumerate(checked_box):
                if self.use_fake:
                    for i, d in enumerate(self.fake_data[checked_box[j]].split(',')):
                        multi.append(int(d.split(':')[0]))
                else:
                    for i, d in enumerate(self.data[checked_box[j]].split(',')):
                        multi.append(int(d.split(':')[0]))
            self.draw_labeled_box(multi)

    # onclick event handler
    def on_click(self, widget):
        if widget == self.label_box:
            self.draw_labeled_box([widget.currentIndex()])
        if widget == self.choose_file:
            directory = self.file_dialog.getExistingDirectory(self, '选取文件夹', '')
            print(directory)
            self.obbs_path = directory
            self.change_obbs(directory)
        if widget == self.display_btn:
            self.draw_multi_obb()
        if widget == self.relation_text:
            index = widget.currentIndex()
            checked_index = self.label_box.get_checked_box()
            if checked_index:
                print(checked_index)
                # print(','.join(checked_index))
                print(str(checked_index), str(index))
        if widget == self.write_btn:
            self.write_txt()
        if widget == self.clear_write_btn:
            self.clear_txt()
        if widget == self.revert_last_state:
            self.back_stack()
        if widget == self.save_relation:
            self.write_single_relation()
        # 没生效
        if widget == self.display_relations_list:
            self.draw_multi_obb(self.relation_stack[self.display_relations_list.currentIndex()])
        if widget == self.display_point:
            self.display_all_point()

    # 删除
    def clear_txt(self):
        self.relation_stack = []
        if self.save_path != '':
            if os.path.isfile(self.save_path):
                os.remove(self.save_path)
        self.use_fake = False

    # 撤销
    def back_stack(self):
        print('back_stack', self.relation_stack)
        self.relation_stack.pop()
        if not self.relation_stack:
            self.use_fake = False
        self.display_all_relations()

    # 保存单个
    def write_single_relation(self):
        # 先压栈
        pair = self.label_box.get_checked_box()
        pair_temp = ''

        if self.use_fake:
            for i, p in enumerate(pair):
                for single in self.fake_data[p].split(','):
                    print(single)
                    pair_temp = pair_temp + '-' + single.split(':')[0]
            pair = pair_temp
        else:
            pair = '-'.join([str(x) for x in pair])
        if len(pair) >= 1:
            index = self.relation_text.currentIndex()
            if (pair, index) not in self.relation_stack:
                self.relation_stack.append((pair, index))
                self.display_all_relations()
        fake_data = []
        record = []
        # 现有的都是-a-b-c 组织起来的
        for (pair, index) in self.relation_stack:
            temp_list = []
            print(pair.split('-'))
            for p in pair.split('-'):
                if p != '':
                    record.append(int(p))
                    temp_list.append(self.data[int(p)])
            fake_data.append(','.join([str(x) for x in temp_list]))
        for i, d in enumerate(self.data):
            if i in record:
                pass
            else:
                fake_data.append(d)
        print(fake_data)
        self.fake_data = fake_data
        self.label_box.fn_init_data(self.fake_data)
        self.use_fake = True

    # 保存

    def write_txt(self):
        path = self.obbs_path
        file_name = path.split('/')[-1] + '_result.txt'
        print(path)
        print(file_name)
        directory = self.file_dialog_write.getExistingDirectory(self, '选取存储位置', '')
        print(directory)
        self.save_path = os.path.join(directory, file_name)
        with open(self.save_path, 'a+')as fp:
            for i, (index, relation) in enumerate(self.relation_stack):
                fp.write(','.join(str(x) for x in index) + ':' + str(relation) + "\n")

    # 画出bbox
    def draw_labeled_box(self, index):
        self.gl_widget.repaint_with_data(index)

    # 更换 bbox
    def change_obbs(self, path):
        self.gl_widget.change_data(path)
        self.data = self.gl_widget.get_label_data()
        print(self.data)
        self.label_box.clear()
        self.label_box.fn_init_data(self.data)

    # 显示所有已保存的关系
    def display_all_relations(self):
        self.display_relations_list.clear()
        for relation in self.relation_stack:
            self.display_relations_list.addItem(str(relation))

    def display_all_point(self):
        self.gl_widget.display_point()
