from PyQt5.QtWidgets import QMainWindow,QLabel,QPushButton,QWidget,QApplication,QVBoxLayout,QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
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
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Медуза")
        self.datalabel = QLabel()
        self.datalabel.setText("Температура: 0°C Кислотность: 0 pH Соль: 0 Кислород: 0 Co2")
        self.setGeometry(0,0,1900,1000)           
        buttonget = QPushButton()
        buttonget.setText("Получить данные")
        buttonget.clicked.connect(self.getdatathread)
        buttonUpdate = QPushButton()
        buttonUpdate.clicked.connect(lambda: self.Updaterservice())
        buttonUpdate.setText("Обновить программу")
        buttonUpdate.setGeometry(0,30,100,40)
        buttonsetip = QPushButton()
        buttonsetip.setText("Изменить IP")
        buttonsetip.clicked.connect(IpAddressSaver.SetIpAddress)
        self.datalabel.move(QApplication.desktop().screen().rect().center()- self.datalabel.rect().center())
        #self.datalabel.setGeometry(385,490,1150,100)
        buttonget.setGeometry(850,560,120,40)
        self.datalabel.setFont(QFont("Arial",23))
        self.timertext = QLabel()
        self.timertext.setGeometry(840,615,500,40)
        Queue1 = Queue()
        Queue2 = Queue()
        Queue1.put(self.GetData)
        Queue2.put(self.timertext)
        waiterthread = threading.Thread(target=self.waiterservice)
        waiterthread.daemon = True
        waiterthread.start()
        queuegetdata = Queue()
        queuegetdata.put(self.getdatathread)
        botthread = threading.Thread(target=lambda: self.starttelebot(queuegetdata))
        botthread.daemon = True
        botthread.start()
        self.waitdatatext = QLabel()
        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout1.addWidget(buttonsetip)
        layout1.addWidget(buttonUpdate)
        layout2.addLayout(layout1)
        layout2.addWidget(self.datalabel)
        layout2.addWidget(self.timertext)
        layout2.addWidget(buttonget)
        layout2.addWidget(self.waitdatatext)       
        widget = QWidget()
        widget.setLayout(layout2)
        self.setCentralWidget(widget)
        self.getdatathread()

    def getdatathread(self):
        thread = threading.Thread(target=self.GetData,daemon=True)
        thread.start()

    def starttelebot(self,queue):
        self.bot = telegrambot.bot(queue)
        self.bot.run()

    def GetData(self):
        self.waitdatatext.setText("Получение данных")
        self.waitdatatext.setFont(QFont("Arial",13))
        temp,acid,salt,oxygen = Request(IpAddressSaver.GetIpAddress())
        self.datalabel.setText(f"Температура: {temp}°C Кислотность: {acid} pH Соль: {salt} Кислород: {oxygen} Co2")
        if(float(temp) > 11 or float(acid) > 8 or float(acid) < 5 or float(salt) > 44):
            self.bot.sendmessage(f"КРИТИЧЕСКИЕ ДАННЫЕ!!!!!! Температура: {temp}°C \n Кислотность: {acid} pH \n Соль: {salt} \n Кислород: {oxygen} Co2")
        else:
            self.bot.sendmessage(f"Температура: {temp}°C \n Кислотность: {acid} pH \n Соль: {salt} \n Кислород: {oxygen} Co2")
        self.waitdatatext.setText("")
        

    def waiterservice(self):
        timer = 3600
        while True:
            time.sleep(1)
            timer -= 1
            self.timertext.setText(f"Получение данных через: {timer} секунд")
            if(timer == 0):
                timer = 3600
                self.GetData()
    def Updaterservice(self):
        import pyautogui
        import Updater
        thread1 = threading.Thread(target=pyautogui.alert,args=("Обновление началось",))
        thread1.daemon = True
        thread1.start()
        time.sleep(1)
        Updater.Update()
        thread2 = threading.Thread(target=pyautogui.alert,args=("Перезапуск программы",))
        thread2.daemon = True
        thread2.start()
        time.sleep(1)
        import sys
        sys.exit()

