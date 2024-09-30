from PyQt5.QtWidgets import QMainWindow,QLabel,QPushButton,QGridLayout,QWidget,QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QSize
from requester import Request
import multiprocessing
import IpAddressSaver

if __name__ == '__main__':
    multiprocessing.freeze_support()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Медуза")
        self.datalabel = QLabel(self)
        self.datalabel.setText("Температура: 0°C Кислотность: 0 pH Соль: 0 Кислород: 0 Co2")
        self.setFixedSize(1920,1080)               
        self.datalabel.setFixedSize(QSize(1150,100))
        buttonget = QPushButton(self)
        buttonget.setText("Получить данные")
        buttonget.clicked.connect(lambda: self.GetData("192.168.15.230"))
        buttonsetip = QPushButton(self)
        buttonsetip.setText("Изменить IP")
        buttonsetip.clicked.connect(IpAddressSaver.SetIpAddress)
        self.datalabel.move(QApplication.desktop().screen().rect().center()- self.datalabel.rect().center())
        self.datalabel.setFont(QFont("Arial",30))
        self.GetData(IpAddressSaver.GetIpAddress())

    def GetData(self,ipaddress):
        temp,acid,salt,oxygen = Request(IpAddressSaver.GetIpAddress())
        self.datalabel.setText(f"Температура: {temp}°C Кислотность: {acid} pH Соль: {salt} Кислород: {oxygen} Co2")

    def waiterservice():
        timer = 3600
