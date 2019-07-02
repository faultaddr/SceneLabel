# coding=utf-8
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.raw.GLUT import *

from core.util import *

from OpenGL.GLUT import *
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QVector3D, QMatrix4x4
import OpenGL.GL as gl
import OpenGL.GLU as glu
from core.camera import Camera
from string import digits

ROOT_PATH = '/data/Liu/obj_data/pc'
logger = get_logger()


class Mesh(object):
    path = ''
    # variable for object
    ver = []
    tri = []
    vn = []
    hier_data = []
    data = []

    def __init__(self, path):
        super(Mesh, self).__init__()
        self.path = path
        ## variable for shading

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
        logger.info(get__function_name() + '-->' + str(self.hier_data))
        hier_group = []
        for data in self.hier_data:
            leaf_group = data['leaf_group']
            room_name = self.path.split('/')[-1].split('.')[0]
            category_name = room_name.translate(str.maketrans('', '', digits))
            single_group = []
            for leaf in leaf_group:
                ver, tri, vn = get_obj_data(os.path.join(os.path.join(os.path.join(ROOT_PATH, category_name),
                                                                      room_name), leaf + '.obj'))
                single_group.append([ver, tri, vn])
            hier_group.append(single_group)
        self.data = hier_group

    def draw_mesh(self):
        """
        function for render input objects
        with material
        """

        self.init_data()
        print(self.path)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        # apply shading
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        # if (self.__shading):
        glShadeModel(GL_SMOOTH)
        # else:
        #     glShadeModel(GL_FLAT)

        # # set material information
        glMaterialfv(GL_FRONT, GL_AMBIENT, self.__ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.__diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, self.__specular)
        glMaterialfv(GL_FRONT, GL_SHININESS, self.__shininess)

        # render objects
        glBegin(GL_TRIANGLES)

        for group in self.data:
            for j, g in enumerate(group):

                ver, tri, vn = g[0], g[1], g[2]

                for i in range(len(tri)):
                    # index
                    id0 = tri[i][0]
                    id1 = tri[i][1]
                    id2 = tri[i][2]
                    # set vertex and  bertex normal
                    # v1
                    glNormal3f(vn[id0][0], vn[id0][1], vn[id0][2])

                    glVertex3f(ver[id0][0], ver[id0][1], ver[id0][2])
                    # v2
                    glNormal3f(vn[id1][0], vn[id1][1], vn[id1][2])
                    glVertex3f(ver[id1][0], ver[id1][1], ver[id1][2])
                    # v3
                    glNormal3f(vn[id2][0], vn[id2][1], vn[id2][2])
                    glVertex3f(ver[id2][0], ver[id2][1], ver[id2][2])

        glEnd()
        glFlush()
        glPopMatrix()
