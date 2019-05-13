from PyQt5.QtGui import QMatrix4x4, QVector3D
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np


class Cube(object):
    LEN = 0.5
    N_VERTEX = 24
    bbox_array = np.loadtxt('test.obb')

    VERTICES = np.array([
        (1, -1, -1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, -1),
        (1, -1, 1),
        (1, 1, 1),
        (-1, -1, 1),
        (-1, 1, 1)

    ], dtype=np.float32) * LEN

    EDGES = np.array([
        (0, 1),
        (0, 3),
        (0, 4),
        (2, 1),
        (2, 3),
        (2, 7),
        (6, 3),
        (6, 4),
        (6, 7),
        (5, 1),
        (5, 4),
        (5, 7)
    ], dtype=np.uint8)

    def __init__(self, size=1, pose=None):
        self.size = size
        self.pose = QMatrix4x4() if pose is None else QMatrix4x4(pose)

    def draw(self):
        glPushMatrix()
        glBegin(GL_LINES)
        for array in self.bbox_array:
            for edge in self.EDGES:
                for vertex in edge:
                    glVertex3f(array[vertex][0], array[vertex][1], array[vertex][2])
        glEnd()
        glPopMatrix()
