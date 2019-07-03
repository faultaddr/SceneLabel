from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from core.ComboCheckBox import ComboCheckBox
from liu.mesh_widget import GLWidget
from core.util import get_logger, get__function_name, get_label_info


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        # widget init
        self.gl_widget = GLWidget(self)
        self.display_mesh = QPushButton('显示面片')
        self.choose_file = QPushButton('选取文件')
        self.file_dialog = QFileDialog()
        self.label_box = ComboCheckBox()
        self.display_relations_list = QListWidget()
        self.merge_mesh_button = QPushButton('合并面片')
        self.merge_name = QLineEdit()
        # init
        self.json_data_path = ''
        self.json_data = []
        self.operation_stack = []

        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.gl_widget)

        # child layout
        child_layout_v_1 = QVBoxLayout()
        child_layout_h_1 = QHBoxLayout()
        child_layout_h_2 = QHBoxLayout()
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
        self.label_box.currentIndexChanged.connect(lambda: self.on_click(self.label_box))
        # display combined group
        self.display_relations_list.currentItemChanged.connect(lambda: self.display_all_relations())

        # merge the group
        self.merge_mesh_button.clicked.connect(lambda: self.on_click(self.merge_mesh_button))

        child_layout_h_1.addWidget(self.choose_file, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_1.addWidget(self.display_mesh, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_1.addWidget(self.label_box, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_2.addWidget(self.merge_name, 0, Qt.AlignLeft | Qt.AlignTop)
        child_layout_h_2.addWidget(self.merge_mesh_button, 0, Qt.AlignLeft | Qt.AlignTop)

        child_layout_v_1.addLayout(child_layout_h_1, 1)
        child_layout_v_1.addLayout(child_layout_h_2, 1)
        main_layout.addLayout(child_layout_v_1)
        self.setLayout(main_layout)
        self.setWindowTitle("Label Tools")
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_click(self, widget):
        if widget == self.display_mesh:
            index = self.label_box.get_checked_box()
            self.draw_labeled_mesh(index)
        if widget == self.choose_file:
            directory = self.file_dialog.getOpenFileName(self, '选取文件夹')
            self.json_data_path = directory[0]
            self.change_mesh(directory[0])
        if widget == self.merge_mesh_button:
            name = self.merge_name.text()
            if name != '':
                index = self.label_box.get_checked_box()
                self.opt_merge(index)

    def change_label(self):
        get_logger().info(get__function_name() + '-->')
        label_list = get_label_info(self.json_data_path)
        self.label_box.clear()
        self.label_box.fn_init_data(label_list)

    def change_mesh(self, path):
        self.gl_widget.change_data(path)
        self.change_label()

    def draw_labeled_mesh(self, index_list):
        self.gl_widget.repaint_with_data(index_list)

    def display_all_relations(self):
        self.display_relations_list.clear()
        for operation in self.operation_stack:
            self.display_relations_list.addItem(str(operation))

    def opt_merge(self, index):
        # TODO 1.build a buffer to store the operation
        # TODO 2.recursively change the parent of the under merged mesh to the new one
        # TODO 3.in the end write the new json format doc to represent ground truth

