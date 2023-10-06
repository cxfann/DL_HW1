import sys
import random
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
        self.label_a = None
        self.label_b = None

        self.input_c = None

        self.num_c = -1

    def show_A(self):
        if self.window_a is None:
            self.window_a = QMainWindow()
            ui = UiA()
            ui.setupUi(self.window_a)
            ui.pushButton.clicked.connect(self.show_B)
            ui.pushButton_2.clicked.connect(self.show_C)
            self.label_a = ui.label

        result = random.randint(0, 100)
        self.label_a.setText(str(result))

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
            self.label_b = ui.labeltest
        

        self.label_b.setText(str(self.num_c))
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
            ui.pushButton.clicked.connect(self.handle_C)
            self.input_c = ui.input_c
        
        self.window_c.show()
        if self.window_a is not None:
            self.window_a.close()
        if self.window_b is not None:
            self.window_b.close()

    def handle_C(self):
        number = self.input_c.text()
        if number.strip():
            self.num_c = int(number)
            self.show_A()
        else:
            pass

    def run(self):
        self.show_A()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    controller = Controller()
    controller.run()