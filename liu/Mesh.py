# coding=utf-8
from string import digits

from OpenGL.GL import *
from OpenGL.GLUT import *

from core.util import get_json_data, get_logger, get_obj_data, get__function_name

ROOT_PATH = '/data/Liu/obj_data/pc'
logger = get_logger()


class Mesh(object):
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
    # light info
    light_ambient = [0.25, 0.25, 0.25]
    light_diffuse = [1.0, 1.0, 1.0]
    light_specular = [1.0, 1.0, 1.0]
    light_position = [0, 0, 1, 1]
    light = [light_ambient, light_diffuse, light_specular, light_position]

    def __init__(self, path):
        super(Mesh, self).__init__()

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
        self.hier_data = get_json_data(self.path)
        self.hier_display_index = range(0, len(self.hier_data))
        logger.info(get__function_name() + '-->' + 'init_data()' + 'hier_data:' + str(self.hier_data))
        self.change_data()

    def change_data(self):
        all_data = []
        for i, data in enumerate(self.hier_data):
            if i in self.hier_display_index:
                leaf_group = data['leaf_group']
                room_name = self.path.split('/')[-1].split('.')[0].split('_')[0]
                category_name = room_name.translate(str.maketrans('', '', digits))
                single_group = []
                for leaf in leaf_group:
                    ver, tri, vn = get_obj_data(os.path.join(os.path.join(os.path.join(ROOT_PATH, category_name),
                                                                          room_name), leaf + '.obj'))
                    single_group.append([ver, tri, vn])
                all_data.append(single_group)
        self.data = all_data
        self.buffers_list, self.lens = self.create_vbo()
        self.record_path = self.path

    def create_vbo(self):
        if self.data:
            buffers_list = []
            lens = []
            for d in self.data:
                for i in d:
                    ver = []
                    tri = []
                    vn = []
                    for a in i[0]:
                        ver.extend([k / 100 for k in a])
                    for b in i[1]:
                        tri.extend(b)
                    for c in i[2]:
                        vn.extend(c)
                    buffers = glGenBuffers(3)
                    glBindBuffer(GL_ARRAY_BUFFER, buffers[0])
                    glBufferData(GL_ARRAY_BUFFER,
                                 (ctypes.c_float * len(ver))(*ver),
                                 GL_STATIC_DRAW)
                    glBindBuffer(GL_ARRAY_BUFFER, buffers[1])
                    glBufferData(GL_ARRAY_BUFFER,
                                 (ctypes.c_float * len(vn))(*vn),
                                 GL_STATIC_DRAW)
                    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffers[2])
                    glBufferData(GL_ELEMENT_ARRAY_BUFFER,
                                 (ctypes.c_int * len(tri))(*tri),
                                 GL_STATIC_DRAW)
                    buffers_list.append(buffers)
                    lens.append(len(tri))
            return buffers_list, lens
        else:
            return [], 0

    def draw(self):

        # turn on shading
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_NORMALIZE)

        # set lighting information
        glLightfv(GL_LIGHT0, GL_AMBIENT, self.light_ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.light_diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, self.light_specular)
        glLightfv(GL_LIGHT0, GL_POSITION, self.light_position)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glShadeModel(GL_SMOOTH)

        #  set material information
        glMaterialfv(GL_FRONT, GL_AMBIENT, self.__ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.__diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, self.__specular)
        glMaterialfv(GL_FRONT, GL_SHININESS, self.__shininess)
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
                glBindBuffer(GL_ARRAY_BUFFER, buffers[0])
                glVertexPointer(3, GL_FLOAT, 0, None)
                glBindBuffer(GL_ARRAY_BUFFER, buffers[1])
                glNormalPointer(GL_FLOAT, 0, None)
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffers[2])
                glDrawElements(GL_TRIANGLES, lens[i], GL_UNSIGNED_INT, None)
