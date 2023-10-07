from ui_jump import *


if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = MainWindow(app)
    controller.show()
    sys.exit(app.exec_())