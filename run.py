import sys

from OpenGL.GLUT import glutInit, glutInitDisplayMode, GLUT_DOUBLE, GLUT_RGB
from PyQt5.QtWidgets import QApplication

from viewer.window_viewer import Window
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--path")
parser.add_argument("--obb_path")
args = parser.parse_args()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    window = Window(args.path, args.obb_path)
    window.show()
    sys.exit(app.exec_())
