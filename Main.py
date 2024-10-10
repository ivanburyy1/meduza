import multiprocessing
import Interface
import sys
from PyQt5.QtWidgets import QApplication

def InterfaceStart():
    app = QApplication(sys.argv)
    window = Interface.MainWindow()
    window.showMaximized()

    sys.exit(app.exec())




if __name__ == '__main__':
    multiprocessing.freeze_support()
    inter = multiprocessing.Process(target=InterfaceStart)
    inter.start()
    inter.join()