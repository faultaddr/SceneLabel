import sys

from OpenGL.GLUT import glutInit, glutInitDisplayMode, GLUT_DOUBLE, GLUT_RGB
from PyQt5.QtWidgets import QApplication

from s3dis.window_s3dis import MainWindow
# from core.window import Window
from liu.window_liu import Window

if __name__ == '__main__':
    app = QApplication(sys.argv)
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    window = MainWindow()
    # window = Window()
    window.show()
    sys.exit(app.exec_())
