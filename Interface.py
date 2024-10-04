from PyQt5.QtWidgets import QMainWindow,QLabel,QPushButton,QGridLayout,QWidget,QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QSize
from requester import Request
import threading
import IpAddressSaver
from queue import Queue
import time
import telegrambot

if __name__ == '__main__':
    print("Запустите Main.py")

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
        buttonget.clicked.connect(self.GetData)
        buttonsetip = QPushButton(self)
        buttonsetip.setText("Изменить IP")
        buttonsetip.clicked.connect(IpAddressSaver.SetIpAddress)
        self.datalabel.move(QApplication.desktop().screen().rect().center()- self.datalabel.rect().center())
        buttonget.setGeometry(850,560,120,40)
        self.datalabel.setFont(QFont("Arial",23))
        self.timertext = QLabel(self)
        self.timertext.setGeometry(840,615,500,40)
        Queue1 = Queue()
        Queue2 = Queue()
        Queue1.put(self.GetData)
        Queue2.put(self.timertext)
        waiterthread = threading.Thread(target=self.waiterservice)
        waiterthread.daemon = True
        waiterthread.start()
        queuegetdata = Queue()
        queuegetdata.put(self.GetData)
        botthread = threading.Thread(target=lambda: self.starttelebot(queuegetdata))
        botthread.daemon = True
        botthread.start()
        self.GetData()

    def starttelebot(self,queue):
        self.bot = telegrambot.bot(queue)
        self.bot.run()
    def GetData(self):
        temp,acid,salt,oxygen = Request(IpAddressSaver.GetIpAddress())
        self.datalabel.setText(f"Температура: {temp}°C Кислотность: {acid} pH Соль: {salt} Кислород: {oxygen} Co2")
        self.bot.sendmessage(f"Температура: {temp}°C \n Кислотность: {acid} pH \n Соль: {salt} \n Кислород: {oxygen} Co2")
        

    def waiterservice(self):
        timer = 3600
        while True:
            time.sleep(1)
            timer -= 1
            self.timertext.setText(f"Получение данных через: {timer} секунд")
            if(timer == 0):
                timer = 3600
                self.GetData()
