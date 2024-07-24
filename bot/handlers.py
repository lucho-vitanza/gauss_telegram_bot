import telebot
from config import TOKEN
from database import session, User, Audio

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Ingresar al servicio')
    btn2 = telebot.types.KeyboardButton('Registrar un nuevo medico')
    btn3 = telebot.types.KeyboardButton('Tutorial de uso')
    keyboard.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, 'Seleccione una opción:', reply_markup=keyboard)

# Agregar más manejadores aquí

def run_bot():
    bot.polling()


