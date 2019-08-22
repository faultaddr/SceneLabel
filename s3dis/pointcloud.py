# coding=utf-8
import threading
from concurrent.futures import ProcessPoolExecutor

import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *

from core.util import get_logger, get_s3dis_json_data, json_2_obj
import datetime
from cachetools import LRUCache, RRCache, cachedmethod, cached, TTLCache

ROOT_PATH = '/data/S3DIS/Stanford3dDataset_v1.2_Aligned_Version/Area_1/'
logger = get_logger()
cache = TTLCache(maxsize=400, ttl=300)


def process_data(d):
    data = eval(d)
    if data['parent'] == -1:
        instance_path = data['path']
        instance_label = data['label']
        v = []
        c = []
        mean_xyz = [0, 0, 0]
        for instance in instance_path:
            original_data = np.loadtxt(instance)
            vex = original_data[:, :3]
            mean_xyz = np.mean(vex, axis=0)
            color = original_data[:, 3:]
            vex = np.reshape(vex, (1, -1))
            color = np.reshape(color, (1, -1))
            color = color / 255
            v.extend(vex.tolist()[0])
            c.extend(color.tolist()[0])
        return (v, c), instance_label, mean_xyz, data['id']


class PC(object):
    path = ''
    # variable for object
    ver = []
    tri = []
    vn = []
    hier_data = []
    hier_display_index = []
    hier_display_id = []
    data = []
    buffers_list = None
    lens = []
    record_path = ''
    label_list = []
    mean = []
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

        self.hier_display_id = []
        all_data = []
        all_label = []
        mean_xyz = [0, 0, 0]

        start_time = datetime.datetime.now()
        pool = ProcessPoolExecutor(max_workers=16)
        result = list(pool.map(process_data, [str(y) for y in self.hier_data]))
        for r in result:
            if r is not None:
                (v, c), instance_label, mean, i_id = r
                all_data.append((v, c))
                all_label.append(instance_label)
                mean_xyz.append(mean)
                self.hier_display_id.append(i_id)

        self.hier_display_index = range(0, len(all_data))
        # v = np.reshape(np.array(v), (1, -1))
        # c = np.reshape(np.array(c), (1, -1))

        self.mean = np.sum(np.array(mean_xyz), axis=0) / len(all_data)
        self.data = all_data
        self.buffers_list, self.lens = self.create_vbo(str(self.hier_display_id))
        self.record_path = self.path
        self.label_list = all_label
        end_time = datetime.datetime.now()
        print((end_time - start_time).seconds)

    def create_vbo(self, id_list_str):
        if self.data:
            buffers_list = []
            lens = []
            for single_data in self.data:
                vex = single_data[0]
                color = single_data[1]
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
