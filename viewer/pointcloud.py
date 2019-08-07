# coding=utf-8

import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL._bytes import as_8_bit
from core.util import get_logger, get_ply_data_origin
import json

ROOT_PATH = '/data/S3DIS/Stanford3dDataset_v1.2_Aligned_Version/Area_1/'
logger = get_logger()


class PC(object):
    path = ''
    obb_path = ''
    # variable for object
    ver = []
    tri = []
    vn = []
    points = []
    colors = []
    buffers_list = None
    lens = 0
    mean = [0, 0, 0]
    det_list = []
    obb_list = []
    label_list = []
    p_list = []
    color_data = []

    # light info

    def __init__(self, path):
        super(PC, self).__init__()
        self.path = path

    def init_data(self):
        print(self.path)
        detection = self.obb_path
        self.det_list = np.loadtxt(detection)
        print(self.det_list[0])
        if isinstance(self.det_list[0].tolist(), list):
            for det in self.det_list:
                print('---', det)
                self.obb_list.append(det[0:4])
                self.label_list.append(det[4])
                self.p_list.append(det[5])
        else:
            print("not list")
            self.obb_list.append(self.det_list[0:4])
            self.label_list.append(self.det_list[4])
            self.p_list.append(self.det_list[5])

        self.points, self.colors = get_ply_data_origin(self.path)
        # self.points = self.points / 4000
        print(np.max(self.points, axis=0), np.min(self.points, axis=0))
        min_ = np.min(self.points, axis=0)
        self.points = self.points - min_
        for i, obb in enumerate(self.obb_list):
            self.obb_list[i][0] = obb[0] - min_[1]
            self.obb_list[i][1] = obb[1] - min_[0]
            self.obb_list[i][2] = obb[2] - min_[1]
            self.obb_list[i][3] = obb[3] - min_[0]
        max_xyz = np.max(self.points, axis=0)
        min_xyz = np.min(self.points, axis=0)
        print(max_xyz)
        print(min_xyz)
        self.points = self.points / (max_xyz - min_xyz)
        for i, obb in enumerate(self.obb_list):
            self.obb_list[i][0] = obb[0] / (max_xyz[1] - min_xyz[1])
            self.obb_list[i][2] = obb[2] / (max_xyz[1] - min_xyz[1])
            self.obb_list[i][1] = obb[1] / (max_xyz[0] - min_xyz[0])
            self.obb_list[i][3] = obb[3] / (max_xyz[0] - min_xyz[0])
        self.mean = np.mean(self.points, axis=0)
        print(self.mean)
        with open('part_color_mapping.json')as f:
            self.color_data = json.load(f)

        # self.buffers_list, self.lens = self.create_vbo()

    # def create_vbo(self):
    #     if self.points.tolist():
    #         buffers_list = []
    #         point = []
    #         color = []
    #         print(self.points.tolist())
    #         for a in self.points.tolist():
    #             point.append(a[0])
    #             point.append(a[1])
    #             point.append(a[2])
    #         for c in self.colors.tolist():
    #             color.append(c[0] * 255)
    #             color.append(c[1] * 255)
    #             color.append(c[2] * 255)
    #         print(point)
    #         print(color)
    #         index = np.arange(len(point))
    #         print(index)
    #         buffers = glGenBuffers(3)
    #         glBindBuffer(GL_ARRAY_BUFFER, buffers[0])
    #         glBufferData(GL_ARRAY_BUFFER, (ctypes.c_float * len(point))(*point), GL_STATIC_DRAW)
    #         glBindBuffer(GL_ARRAY_BUFFER, buffers[1])
    #         glBufferData(GL_ARRAY_BUFFER, (ctypes.c_float * len(color))(*color), GL_STATIC_DRAW)
    #         glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffers[2])
    #         glBufferData(GL_ELEMENT_ARRAY_BUFFER,
    #                      (ctypes.c_int * len(index))(*index),
    #                      GL_STATIC_DRAW)
    #         print(buffers)
    #         buffers_list.append(buffers)
    #         lens = len(point)
    #         return buffers_list, lens
    #     else:
    #         return [], 0

    def draw(self):
        self.draw_mesh()

    def draw_mesh(self):
        """
        function for render input objects
        with material
        """
        # if self.lens == 0:
        #     print('----init')
        #     self.init_data()
        # else:
        #     print('---')
        #     buffers_list, lens = self.buffers_list, self.lens
        #     for buffers in buffers_list:
        #         print(lens)
        #         glBindBuffer(GL_ARRAY_BUFFER, buffers[0])
        #         glVertexPointer(3, GL_FLOAT, 0, None)
        #         glBindBuffer(GL_ARRAY_BUFFER, buffers[1])
        #         glColorPointer(3, GL_FLOAT, 0, None)
        #         glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffers[2])
        #         glDrawElements(GL_POINTS, lens, GL_UNSIGNED_INT, None)
        indices = np.arange(0, len(self.points))
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glPointSize(3)
        glVertexPointer(3, GL_FLOAT, 0, self.points.tolist())
        glColorPointer(3, GL_FLOAT, 0, self.colors.tolist())
        glDrawElements(GL_POINTS, len(indices), GL_UNSIGNED_INT, indices)
        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)
        glLineWidth(3)
        glBegin(GL_LINES)
        min_z = np.min(self.points, axis=0)[2]
        max_z = np.max(self.points, axis=0)[2]
        avg_z = (min_z + max_z) / 2
        xy_list = []
        for i, obb in enumerate(self.obb_list):
            print(obb)
            y1, x1, y2, x2 = obb[0], obb[1], obb[2], obb[3]
            y1, x1, y2, x2 = y1, x1, y2, x2
            label = self.label_list[i]
            p_label = self.p_list[i]
            xy_list.append([(x1 + x2) / 2, (y1 + y2) / 2, p_label])
            glColor3f(self.color_data[int(label)][0], self.color_data[int(label)][1],
                      self.color_data[int(label)][2])

            glVertex3f(x2, y2, avg_z)
            glVertex3f(x1, y2, avg_z)
            glVertex3f(x2, y2, avg_z)
            glVertex3f(x2, y1, avg_z)
            glVertex3f(x2, y1, avg_z)
            glVertex3f(x1, y1, avg_z)
            glVertex3f(x1, y1, avg_z)
            glVertex3f(x1, y2, avg_z)
        glEnd()
        for s in xy_list:
            # glTranslatef(s[0], s[1], avg_z)
            # 设置颜色为绿色
            glColor3f(0.0, 1.0, 0.0)
            # 定位文字
            glRasterPos3f(s[0], s[1], avg_z)
            self.draw_text(str(s[2])[0:4])

    # 绘制文字函数
    def draw_text(self, string):
        # 循环处理字符串
        for c in string:
            # 输出文字
            glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(c))
