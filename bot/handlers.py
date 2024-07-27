import telebot
from config import TOKEN
from telebot import types
import os
import threading
import json

bot = telebot.TeleBot(TOKEN)

estado_usuario = {}

#Ruta donde voy a guardar los audios, es relativo desde donde se ejecuta el script main.py

audio_folder = './audios'



def send_menu(chat_id, text):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Ingresar al servicio')
    btn2 = telebot.types.KeyboardButton('Registrar un nuevo medico')
    btn3 = telebot.types.KeyboardButton('Tutorial de uso')
    keyboard.add(btn1, btn2, btn3)
    bot.send_message(chat_id, text, reply_markup=keyboard)
    reset_timer(chat_id, text)  # Resetear el temporizador al enviar el menú

def send_service_menu(chat_id, text):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn_send_audio = telebot.types.KeyboardButton('Enviar audio')
    btn_cancel_audio = telebot.types.KeyboardButton('Cancelar último audio')
    btn_logout = telebot.types.KeyboardButton('Cerrar sesión')
    keyboard.add(btn_send_audio, btn_cancel_audio, btn_logout)
    bot.send_message(chat_id, text, reply_markup=keyboard)
    reset_timer(chat_id, text)  # Resetear el temporizador al enviar el menú de servicio


#----------------------TIMER------------------------------

timers = {}

def reset_timer(chat_id, text):
    global timers
    
    # Cancelar el temporizador existente si existe
    if chat_id in timers:
        timers[chat_id].cancel()
    
    # Crear un nuevo temporizador para reiniciar el bot después de 10 minutos de inactividad
    timer = threading.Timer(600, send_service_menu, args=[chat_id, text])
    timers[chat_id] = timer
    timer.start()

#------------------------Manejo del comando /start

@bot.message_handler(commands=['start', 'Hola'])

def start_message(message):
    send_menu(message.chat.id, 'Seleccione una opción:')

#-----------------------Manejo de la opción "Ingresar al servicio"

@bot.message_handler(func=lambda message: message.text == 'Ingresar al servicio')
def ingresar_servicio(message):
    
    user_id = message.chat.id
    estado_usuario[user_id] = None

    bot.send_message(message.chat.id, 'Por favor, ingrese su número de ID:')
    bot.register_next_step_handler(message, validar_id)

def validar_id(message):
    user_id = message.text
    # Aquí deberías validar el ID con la base de datos
    # Por ahora, asumimos que el ID es válido
    send_service_menu(message.chat.id, 'ID validado correctamente. Seleccione una opción:')

    return user_id





#------------------------ Manejo de la opción "Registrar un nuevo medico"

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




#------------------- Manejo de la opción "Tutorial de uso"
@bot.message_handler(func=lambda message: message.text == 'Tutorial de uso')

def tutorial_uso(message):
    tutorial_link = 'http://example.com/tutorial'  # Enlace al tutorial
    bot.send_message(message.chat.id, f'Aquí está el tutorial de uso: {tutorial_link}')



#------------------Manejo de la opción "Enviar audio"   

@bot.message_handler(func=lambda message: message.text == 'Enviar audio')


def enviar_audio(message):
    bot.send_message(message.chat.id, 'Por favor, envíe el audio:')
    bot.register_next_step_handler(message, procesar_audio)

def procesar_audio(message):
    if message.content_type == 'voice':
        file_id = message.voice.file_id
    elif message.content_type == 'audio':
        file_id = message.audio.file_id
    else:
        bot.send_message(message.chat.id, 'Formato de archivo no soportado. Por favor, envíe un mensaje de voz o un archivo de audio.')
        return

    user_id = message.chat.id

    guardar_audio(file_id,message,audio_folder)

    guardar_estado(user_id,file_id)
        
    send_service_menu(message.chat.id, 'Seleccione una opción:')

# Manejo de la opción "Cancelar el último audio"

@bot.message_handler(func=lambda message: message.text == 'Cancelar el último audio')

def cancelar_audio(message,audio_folder):

    user_id = message.chat.id
    try:
        with open('estado.json', 'r') as file:
            estado = json.load(file)

    except FileNotFoundError:
        estado = {}

    file_id = estado.pop(user_id, None)

    if file_id:
        file_path = os.path.join(audio_folder, f"{file_id}.ogg")
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print(f"El archivo {file_path} no existe.")
        
        with open('estado.json', 'w') as file:
            json.dump(estado, file)
        
        bot.send_message(message.chat.id, 'Último audio cancelado.')
    else:
        bot.send_message(message.chat.id,'No se encontró ningún audio para cancelar.')

    send_service_menu(message.chat.id, 'Seleccione una opción:')

# Manejo de la opción "Cerrar sesión"
@bot.message_handler(func=lambda message: message.text == 'Cerrar sesión')

def cerrar_sesion(message):
    bot.send_message(message.chat.id, 'Sesión cerrada. Volviendo al menú principal.')
    send_menu(message.chat.id, 'Seleccione una opción:')


def guardar_audio(file_id,message,audio_folder):

    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)


    #Por si no esta creada la carpeta
    if not os.path.exists(audio_folder):
        os.makedirs(audio_folder)    

    file_path = os.path.join(audio_folder, f"{file_id}.ogg")
    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    bot.send_message(message.chat.id, 'Audio recibido con éxito y guardado en el servidor.')

def guardar_estado(user_id, file_id):
    try:
        with open('estado.json', 'r') as file:
            estado = json.load(file)
    except FileNotFoundError:
        estado = {}

    estado[user_id] = file_id

    with open('estado.json', 'w') as file:
        json.dump(estado, file)



def run_bot():
    bot.polling()
