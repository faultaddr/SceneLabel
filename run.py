import sys
from PyQt5.QtWidgets import QApplication

from core import Window


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())