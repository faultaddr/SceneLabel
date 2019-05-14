# coding=utf-8
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.raw.GLUT import *

from core.util import *


class Cube(object):
    LEN = 0.5
    N_VERTEX = 24
    v = get_room_data()
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
        pass

    def draw(self, update=None):
        if update is not None:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glPushMatrix()

            glBegin(GL_LINES)

            for i, array in enumerate(self.v):
                if i == update:
                    glColor3f(0, 1, 0)
                else:
                    glColor3f(1, 0, 0)
                for edge in self.EDGES:
                    for vertex in edge:
                        glVertex3f(array[vertex][0], array[vertex][1], array[vertex][2])
            glEnd()
            glPopMatrix()
        else:
            glPushMatrix()
            glBegin(GL_LINES)
            glColor3f(1, 0, 0)
            for array in self.v:
                for edge in self.EDGES:
                    for vertex in edge:
                        glVertex3f(array[vertex][0], array[vertex][1], array[vertex][2])
            glEnd()
            glPopMatrix()
