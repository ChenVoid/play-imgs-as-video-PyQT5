import sys

from PyQt5.QtWidgets import QApplication

from PlayImg import PlayImg

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = PlayImg()
    MainWindow.show()
    sys.exit(app.exec_())