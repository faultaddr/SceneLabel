# coding=utf-8

import OpenGL.GL as gl
import OpenGL.GLU as glu
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QVector3D, QMatrix4x4
from PyQt5.QtWidgets import QOpenGLWidget, QApplication

from core.camera import Camera
from core.util import *
from s3dis.pointcloud import PC

ROOT_PATH = '/data/Liu/obj_data/pc'
logger = get_logger()


class GLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        self.lastZ = 10
        self.cam = Camera(50.0, 0.1, 100)
        self.cam.lookAt(QVector3D(-11.34805872, 10.68026085, 10.29478443),
                        QVector3D(-11.34805872, 10.68026085, 1.29478443), QVector3D(-1, 1, 1))
        self.rotCenter = QVector3D(0, 0, 0)
        self.data = None
        self.pointcloud = PC(path='')
        self.is_point = False
        self.desktop = QApplication.desktop()

        self.screenRect = self.desktop.screenGeometry()

    def minimumSizeHint(self):

        return QSize(int(self.screenRect.width() / 2), int(self.screenRect.height() / 2))

    def sizeHint(self):
        return QSize(1600, 800)

    def initializeGL(self):
        gl.glClearColor(0.3, 0.3, 0.3, 1.0)
        gl.glClearDepth(1.0)
        gl.glEnable(gl.GL_DEPTH_TEST)

    def resizeGL(self, width, height):
        # gl.glGetError()    # uncomment this line when error occurs here
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadMatrixf(self.cam.perspective(width, height).data())
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def change_data(self, path):
        logger.info(get__function_name() + '-->')
        self.pointcloud.path = path
        self.pointcloud.init_data()
        self.cam.lookAt(QVector3D(self.pointcloud.mean[0], self.pointcloud.mean[1], self.pointcloud.mean[2] * 20),
                        QVector3D(self.pointcloud.mean[0], self.pointcloud.mean[1], self.pointcloud.mean[2]),
                        QVector3D(self.pointcloud.mean[0] / abs(self.pointcloud.mean[0]),
                                  self.pointcloud.mean[1] / abs(self.pointcloud.mean[1]),
                                  self.pointcloud.mean[2] / abs(self.pointcloud.mean[2])))
        self.update()

    def repaint_with_data(self, data):
        logger.info(get__function_name() + '-->' + str(data))
        # logger.info(get__function_name() + '-->' + str(self.pointcloud.hier_data))
        if self.pointcloud.hier_data:
            self.pointcloud.hier_display_index = data
            self.update()

    def paintGL(self):
        logger.info(get__function_name() + '-->')
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadMatrixf(self.cam.modelView.data())

        # enable drawing vertices and color array
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)

        # draw all key frames
        self.pointcloud.draw()

        # disable drawing vertices and color array
        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
        gl.glDisableClientState(gl.GL_COLOR_ARRAY)

    def mousePressEvent(self, event):
        logger.info(get__function_name() + '-->')
        self.lastPos = event.pos()
        self.rotCenter = self.getRotCenter(event.x(), event.y())

    def mouseMoveEvent(self, event):
        logger.info(get__function_name() + '-->')
        x, y = event.x(), event.y()
        dx = x - self.lastPos.x()
        dy = y - self.lastPos.y()
        magnitude = dx ** 2 + dy ** 2

        if magnitude < 50 ** 2:
            # left right moving
            if event.buttons() & Qt.LeftButton:
                newPoint = self.pixelUnproject(x, y, self.lastZ)  # get 3d point that mouse clicks at
                diff = newPoint - self.rotCenter  # calculate distance between rotation center and current point
                t = QVector3D(diff.x(), -diff.y(), 0)  # x -> left&right, y -> up&down
                self.cam.move(t)
                print(self.cam.far, self.cam.near, self.cam.fov)
                self.rotCenter = newPoint
            # rotation
            elif event.buttons() & Qt.RightButton:
                angles = QVector3D(dy, dx, 0)
                self.cam.rotate(angles, self.rotCenter)

        self.lastPos = event.pos()
        self.update()

    def wheelEvent(self, event):
        logger.info(get__function_name() + '-->')
        scroll = event.angleDelta().y()
        if scroll > 0: scroll = 1
        if scroll < 0: scroll = -1

        self.rotCenter = self.getRotCenter(event.x(), event.y())
        self.cam.zoom(self.rotCenter * scroll)
        self.update()

    def getMouseDir(self, winx, winy):
        logger.info(get__function_name() + '-->')
        x = winx * 2.0 / self.width() - 1
        y = 1 - winy * 2.0 / self.height()
        direction = self.cam.projectViewInv * QVector3D(x, y, 1.0)
        return direction.normalized()

    def getRotCenter(self, winx, winy):
        logger.info(get__function_name() + '-->')
        half_patch = 17
        patch_size = half_patch * 2 + 1
        winX, winY = self.fixAppleBug(winx, self.height() - winy)

        self.makeCurrent()
        depths = gl.glReadPixels(winX - half_patch,
                                 winY - half_patch,
                                 patch_size,
                                 patch_size,
                                 gl.GL_DEPTH_COMPONENT,
                                 gl.GL_FLOAT)

        min_depth = depths.min()
        if min_depth == 1: min_depth = self.lastZ
        if min_depth != 1: self.lastZ = min_depth

        return self.pixelUnproject(winx, winy, min_depth)

    def pixelUnproject(self, winx, winy, winz):
        logger.info(get__function_name() + '-->')
        center = glu.gluUnProject(winx, winy, winz,
                                  model=QMatrix4x4().data(),
                                  proj=self.cam.projectView.data(),
                                  view=(0, 0, self.width(), self.height()))
        return QVector3D(*center)

    def fixAppleBug(self, winx, winy):
        logger.info(get__function_name() + '-->')

        return (winx, winy)
