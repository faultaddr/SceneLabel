from PyQt5.QtGui import QMatrix4x4, QQuaternion, QVector3D


class Camera(object):
    """docstring for Camera"""
    CAMERA_ZOOM_STEP = 0.05
    CAMERA_TRAN_STEP = 1
    CAMERA_ROT_STEP = 1

    def __init__(self, fov, near, far):
        self.fov = fov
        self.near = near
        self.far = far
        self._projectView = QMatrix4x4()
        self._modelView = QMatrix4x4()
        self.deltaT = self._defaultTcw()
        self.isFollow = False
        self.lastTarget = None

    def _defaultTcw(self):
        """
        Default camera pose
        --------------------
        Out: QMatrix4x4
        --------------------
        """
        T =  QMatrix4x4()
        T.lookAt(QVector3D(0, -40, 0), QVector3D(0, 0, 0), QVector3D(0, 0, 1))
        return T

    def _move(self, ray):
        """
        Move camera along ray direction
        --------------------
        In: ray -> QVector3D
        --------------------
        """
        T = QMatrix4x4()
        T.translate(ray)
        self._modelView = T * self.modelView

    def perspective(self, width, height):
        """
        Calculate perspective matrix by window width and height
        --------------------
        In: width -> int
            height -> int
        Out: QMatrix4x4
        --------------------
        """
        self._projectView.setToIdentity()
        self._projectView.perspective(self.fov, width / height, self.near, self.far)
        return self.projectView

    def zoom(self, ray):
        """
        Zoom in and zoom out by direction ray
        --------------------
        In: ray -> QVector3D
        --------------------
        """
        self._move(ray * self.CAMERA_ZOOM_STEP)

    def move(self, ray):
        """
        Move by direction ray
        --------------------
        In: ray -> QVector3D
        --------------------
        """
        self._move(ray * self.CAMERA_TRAN_STEP)

    def rotate(self, angles, center):
        """
        Rotate by euler angles at center
        -----------------------
        In: angle -> QVector3D
            center -> QVector3D
        -----------------------
        """
        eulers = QQuaternion.fromEulerAngles(angles)
        R, T = QMatrix4x4(), QMatrix4x4()
        R.rotate(eulers)
        T.translate(center)
        self._modelView = T * R * T.inverted()[0] * self.modelView * self.CAMERA_ROT_STEP

    def lookAt(self, eye, target, direction):
        """
        Set camera pose by eye position, target position and head up direction
        --------------------------
        In: eye -> QVector3D
            target -> QVector3D
            direction -> QVector3D
        --------------------------
        """
        self._modelView.setToIdentity()
        self._modelView.lookAt(eye, target, direction)
        return self.modelView

    def follow(self, pose):
        """
        Follow object at pose
        ----------------------
        In: pose -> QMatrix4x4
        ----------------------
        """
        target = pose.inverted()[0]

        if not self.isFollow:
            self._modelView = self.deltaT * target
            self.isFollow = True
        else:
            deltaT = self.lastTarget * target
            self._modelView = self._modelView * deltaT
    
        self.lastTarget = QMatrix4x4(pose)

    def unfollow(self):
        """Unfollow object"""
        self.isFollow = False

    @property
    def projectView(self):
        return self._projectView

    @property
    def projectViewInv(self):
        return self._projectView.inverted()[0]

    @property
    def modelView(self):
        return self._modelView