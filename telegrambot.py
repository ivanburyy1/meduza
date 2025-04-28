import telebot
import dotenv
import os

class bot:
    def __init__(self,queuegetdata):
        button_request = telebot.types.InlineKeyboardButton("Запросить данные")
        self.keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        self.keyboard.add(button_request)
        self.getdatafunc = queuegetdata.get()

        dotenv.load_dotenv()
        self.bot = telebot.TeleBot(os.environ.get("TELEGRAMBOTKEY"))
        @self.bot.message_handler()
        def getdatabutton(msg : telebot.types.Message):
            while True:
                try:
                    if(msg.from_user.id == int(os.environ.get("USERTOMESSAGE")) and msg.text == "Запросить данные"):
                        print("test")
                        self.getdatafunc()
            
                except:
                    print("Telegram Not responding error")
                    continue
                else:
                    break
        
    def sendmessage(self,message):
        while True:
            try:
                self.bot.send_message(chat_id=os.environ.get("USERTOMESSAGE"),text=message,reply_markup=self.keyboard)
            except:
                print("Telegram Not responding error")
                continue
            else:
                break
    
    def run(self):
        while True:
            try:
                self.bot.polling()
            except:
                print("Telegram bot polling error")
                continue
            else:
             # return to normal operation
                break
            
        
        

if __name__ == '__main__':
    print("Запустите Main.py")