# coding=utf-8

import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *

from core.util import get_logger, get_s3dis_json_data

ROOT_PATH = '/data/S3DIS/Stanford3dDataset_v1.2_Aligned_Version/Area_1/'
logger = get_logger()


class PC(object):
    path = ''
    # variable for object
    ver = []
    tri = []
    vn = []
    hier_data = []
    hier_display_index = []
    data = []
    buffers_list = None
    lens = []
    record_path = ''
    label_list = []

    # light info
    light_ambient = [0.25, 0.25, 0.25]
    light_diffuse = [1.0, 1.0, 1.0]
    light_specular = [1.0, 1.0, 1.0]
    light_position = [0, 0, 1, 1]
    light = [light_ambient, light_diffuse, light_specular, light_position]

    def __init__(self, path):
        super(PC, self).__init__()

        self.path = path
        # variable for shading

        ambient = [0.329412, 0.223529, 0.027451]
        diffuse = [0.780392, 0.568627, 0.113725]
        specular = [0.992157, 0.941176, 0.807843]
        shininess = 128 * 0.21794872
        material = [ambient, diffuse, specular, shininess]
        self.__ambient = material[0]
        self.__diffuse = material[1]
        self.__specular = material[2]
        self.__shininess = material[3]

    def init_data(self):
        self.hier_data = get_s3dis_json_data(self.path)
        self.hier_display_index = range(0, len(self.hier_data))
        self.change_data()

    def change_data(self):
        all_data = []
        all_label = []
        for i, data in enumerate(self.hier_data):
            # room_name = self.path.split('/')[-1].split('.')[0]
            # room_dir = os.path.join(ROOT_PATH, room_name)
            # room_path = os.path.join(room_dir, 'Annotations')\
            instance_path = data['path']
            instance_label = data['label']
            original_data = np.loadtxt(instance_path[0])
            vex = original_data[:, :3]
            vex = np.reshape(vex, (1, -1))
            vex = vex / 50
            color = original_data[:, 3:]
            color = np.reshape(color, (1, -1))
            color = color / 255
            all_data.append((vex, color))
            all_label.append(instance_label)
        self.data = all_data
        self.buffers_list, self.lens = self.create_vbo()
        self.record_path = self.path
        self.label_list = all_label

    def create_vbo(self):
        if self.data:
            buffers_list = []
            lens = []
            for single_data in self.data:
                vex = single_data[0].tolist()[0]
                color = single_data[1].tolist()[0]
                index = np.arange(len(vex))
                buffers = glGenBuffers(3)
                glBindBuffer(GL_ARRAY_BUFFER, buffers[0])
                glBufferData(GL_ARRAY_BUFFER, (ctypes.c_float * len(vex))(*vex), GL_STATIC_DRAW)
                glBindBuffer(GL_ARRAY_BUFFER, buffers[1])
                glBufferData(GL_ARRAY_BUFFER, (ctypes.c_float * len(color))(*color), GL_STATIC_DRAW)
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffers[2])
                glBufferData(GL_ELEMENT_ARRAY_BUFFER,
                             (ctypes.c_int * len(index))(*index),
                             GL_STATIC_DRAW)
                buffers_list.append(buffers)
                lens.append(len(vex))
            return buffers_list, lens
        else:
            return [], 0

    def draw(self):

        # # turn on shading
        # glEnable(GL_LIGHTING)
        # glEnable(GL_LIGHT0)
        # glEnable(GL_NORMALIZE)
        #
        # # set lighting information
        # glLightfv(GL_LIGHT0, GL_AMBIENT, self.light_ambient)
        # glLightfv(GL_LIGHT0, GL_DIFFUSE, self.light_diffuse)
        # glLightfv(GL_LIGHT0, GL_SPECULAR, self.light_specular)
        # glLightfv(GL_LIGHT0, GL_POSITION, self.light_position)
        # glEnable(GL_DEPTH_TEST)
        # glEnable(GL_LIGHTING)
        # glEnable(GL_LIGHT0)
        # glShadeModel(GL_SMOOTH)
        self.draw_mesh()

    def draw_mesh(self):
        """
        function for render input objects
        with material
        """
        if self.lens == 0 or self.record_path != self.path:
            self.init_data()
        buffers_list, lens = self.buffers_list, self.lens
        if lens:
            for i, buffers in enumerate(buffers_list):
                if i in self.hier_display_index:
                    glBindBuffer(GL_ARRAY_BUFFER, buffers[0])
                    glVertexPointer(3, GL_FLOAT, 0, None)
                    glBindBuffer(GL_ARRAY_BUFFER, buffers[1])
                    glColorPointer(3, GL_FLOAT, 0, None)
                    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffers[2])
                    glDrawElements(GL_POINTS, lens[i], GL_UNSIGNED_INT, None)
