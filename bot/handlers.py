import telebot
from config import TOKEN
from telebot import types

bot = telebot.TeleBot(TOKEN)

def send_menu(chat_id, text):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn1 = types.KeyboardButton('Ingresar al servicio')
    btn2 = types.KeyboardButton('Registrar un nuevo medico')
    btn3 = types.KeyboardButton('Tutorial de uso')
    keyboard.add(btn1, btn2, btn3)
    bot.send_message(chat_id, text, reply_markup=keyboard)

def send_service_menu(chat_id, text):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn1 = types.KeyboardButton('Enviar audio')
    btn2 = types.KeyboardButton('Cancelar el último audio')
    btn3 = types.KeyboardButton('Cerrar sesión')
    keyboard.add(btn1, btn2, btn3)
    bot.send_message(chat_id, text, reply_markup=keyboard)

# Manejo del comando /start
@bot.message_handler(commands=['start', 'Hola'])
def start_message(message):
    send_menu(message.chat.id, 'Seleccione una opción:')

# Manejo de la opción "Ingresar al servicio"
@bot.message_handler(func=lambda message: message.text == 'Ingresar al servicio')
def ingresar_servicio(message):
    bot.send_message(message.chat.id, 'Por favor, ingrese su número de ID:')
    bot.register_next_step_handler(message, validar_id)

def validar_id(message):
    user_id = message.text
    # Aquí deberías validar el ID con la base de datos
    # Por ahora, asumimos que el ID es válido
    send_service_menu(message.chat.id, 'ID validado correctamente. Seleccione una opción:')

# Manejo de la opción "Registrar un nuevo medico"
@bot.message_handler(func=lambda message: message.text == 'Registrar un nuevo medico')
def registrar_medico(message):
    msg = bot.send_message(message.chat.id, 'Por favor, ingrese su email:')
    bot.register_next_step_handler(msg, procesar_email)

def procesar_email(message):
    email = message.text
    msg = bot.send_message(message.chat.id, 'Por favor, ingrese su nombre:')
    bot.register_next_step_handler(msg, procesar_nombre, email)

def procesar_nombre(message, email):
    nombre = message.text
    msg = bot.send_message(message.chat.id, 'Por favor, ingrese su apellido:')
    bot.register_next_step_handler(msg, procesar_apellido, email, nombre)

def procesar_apellido(message, email, nombre):
    apellido = message.text
    # Aquí deberías guardar la información del médico en la base de datos
    bot.send_message(message.chat.id, f'Medico registrado con éxito:\nEmail: {email}\nNombre: {nombre}\nApellido: {apellido}')
    send_menu(message.chat.id, 'Seleccione una opción:')

# Manejo de la opción "Tutorial de uso"
@bot.message_handler(func=lambda message: message.text == 'Tutorial de uso')
def tutorial_uso(message):
    tutorial_link = 'http://example.com/tutorial'  # Enlace al tutorial
    bot.send_message(message.chat.id, f'Aquí está el tutorial de uso: {tutorial_link}')

# Manejo de la opción "Enviar audio"
@bot.message_handler(func=lambda message: message.text == 'Enviar audio')
def enviar_audio(message):
    bot.send_message(message.chat.id, 'Por favor, envíe el audio:')
    bot.register_next_step_handler(message, procesar_audio)

def procesar_audio(message):
    audio = message.audio
    # Aquí deberías manejar el audio, por ahora simplemente confirmamos la recepción
    bot.send_message(message.chat.id, 'Audio recibido con éxito.')
    send_service_menu(message.chat.id, 'Seleccione una opción:')

# Manejo de la opción "Cancelar el último audio"
@bot.message_handler(func=lambda message: message.text == 'Cancelar el último audio')
def cancelar_audio(message):
    # Aquí deberías cancelar el último audio
    bot.send_message(message.chat.id, 'Último audio cancelado.')
    send_service_menu(message.chat.id, 'Seleccione una opción:')

# Manejo de la opción "Cerrar sesión"
@bot.message_handler(func=lambda message: message.text == 'Cerrar sesión')
def cerrar_sesion(message):
    bot.send_message(message.chat.id, 'Sesión cerrada. Volviendo al menú principal.')
    send_menu(message.chat.id, 'Seleccione una opción:')

def run_bot():
    bot.polling()
