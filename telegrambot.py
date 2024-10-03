import telebot
import dotenv
import os

class bot:
    def __init__(self):
        button_request = telebot.types.InlineKeyboardButton("Запросить данные")
        self.keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        self.keyboard.add(button_request)

        dotenv.load_dotenv()
        self.bot = telebot.TeleBot(os.environ.get("TELEGRAMBOTKEY"))
        
    def sendmessage(self,message):
        self.bot.send_message(chat_id=os.environ.get("USERTOMESSAGE"),text=message,reply_markup=self.keyboard)
    
    def run(self):
        self.bot.polling()
        

if __name__ == '__main__':
    print("Запустите Main.py")