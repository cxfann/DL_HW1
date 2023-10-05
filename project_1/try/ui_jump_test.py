import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from Ui_A import Ui_MainWindow as UiA
from Ui_B import Ui_MainWindow as UiB
from Ui_C import Ui_MainWindow as UiC

class Controller:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window_a = None
        self.window_b = None
        self.window_c = None

    def show_A(self):
        if self.window_a is None:
            self.window_a = QMainWindow()
            ui = UiA()
            ui.setupUi(self.window_a)
            ui.pushButton.clicked.connect(self.show_B)
            ui.pushButton_2.clicked.connect(self.show_C)
        self.window_a.show()
        if self.window_b is not None:
            self.window_b.close()
        if self.window_c is not None:
            self.window_c.close()

    def show_B(self):
        if self.window_b is None:
            self.window_b = QMainWindow()
            ui = UiB()
            ui.setupUi(self.window_b)
            ui.pushButton.clicked.connect(self.show_C)
        self.window_b.show()
        if self.window_a is not None:
            self.window_a.close()
        if self.window_c is not None:
            self.window_c.close()

    def show_C(self):
        if self.window_c is None:
            self.window_c = QMainWindow()
            ui = UiC()
            ui.setupUi(self.window_c)
            ui.pushButton.clicked.connect(self.show_A)
        self.window_c.show()
        if self.window_a is not None:
            self.window_a.close()
        if self.window_b is not None:
            self.window_b.close()

    def run(self):
        self.show_A()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    controller = Controller()
    controller.run()