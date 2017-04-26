#!/usr/bin/env python
from unidecode import unidecode                                                         # pip install unidecode
import logging                                                                          # Standard python libraries
import telegram                                                                         # pip install python-telegram-bot
from telegram.ext.dispatcher import run_async                                           # python-telegram-bot library
from telegram import InlineKeyboardButton, InlineKeyboardMarkup                         # python-telegram-bot library
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler                  # python-telegram-bot library
from telegram.ext import MessageHandler, Filters                                        # python-telegram-bot library
from time import sleep                                                                  # Standard python libraries
import time                                                                             # Standard python libraries
from echo import echo                                                                   # From file "echo.py"
from sender import sender                                                               # From file "sender.py"
from errores import mensaje_bot, key_b, key_ed, key_o, message_bot, key_eden, key_oen   # From file "errores.py"
from botones import botones                                                             # From file "botones.py"
from database import write_database, read_database                                      # From file "database.py"

# -*- coding: utf-8 -*-

date = time.strftime("%d_%m_%Y")                                                      # Get current date-time for creating the logging file with date info
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',    # Starting logging at WARNING level (for errors information)
                     level=logging.WARNING,
                     filename="bot_log_WARNS--"+date+".log",
                     filemode='w')

# Different InlineKeyboards should be declared before the CommandHandler functions

@run_async
def key_l(bot, update):
    keyboard = [[InlineKeyboardButton("Español 🇪🇸", callback_data='es'),InlineKeyboardButton("English 🇬🇧", callback_data='en')]]

    reply_markup2 = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Elige tu idioma / choose your language:',
      parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup2)

@run_async
def key_l2(bot, update):
    keyboard = [[InlineKeyboardButton("Español 🇪🇸", callback_data='castell'),InlineKeyboardButton("English 🇬🇧", callback_data='glish')]]

    reply_markup2 = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Elige tu idioma / choose your language:',
      parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup2)

@run_async
def key_pr(bot, update):
    keyboard = [[InlineKeyboardButton("Idioma 🗣", callback_data='lang'),InlineKeyboardButton("Sistema operativo ⚙", callback_data='os')]]

    reply_markup2 = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Elige lo que quieres actualizar...',
      parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup2)

@run_async
def key_pren(bot, update):
    keyboard = [[InlineKeyboardButton("Language 🗣", callback_data='langen'),InlineKeyboardButton("Operative system ⚙", callback_data='osen')]]

    reply_markup2 = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Choose what you want to update...',
      parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup2)


@run_async
def start(bot, update):                           # '/start' handler function
  print("\tEjecutando '/start'...")
  user = update.message.from_user['first_name']   # Get username and
  chat_id = update.message.chat_id                # chat_id for basic logging information
  name = unidecode(user)                          # 'username' is always decoded to "utf-8" for avoiding problems with special characters (á,é,í,ó,ú,ñ,😄 (emojis),etc)
  print("Usuario + ID: ",name,chat_id)
  if read_database(chat_id)==None:           # 'read_database' function reads language preferences for choosing a language or other
    bot.sendMessage(chat_id,text="Antes de continuar, debes actualizar tus preferencias de idioma\n\nBefore you continue, you have to update your language preferences")
    lang(bot,update)
  elif 'es' in read_database(chat_id):       # 'es' because of "español"
    bot.sendMessage(chat_id,
        text="Hola "+name+", bienvenido 😄 \n\n*Para descargar una canción puedes:*\nEnviarme el *NOMBRE Y ARTISTA 🎤*\n_LA URL DE LA CANCIÓN 🎶_\nUtiliza /vid _PARA BUSCAR TUS CANCIONES_ 🔍\n\nPara descubir _más sobre el bot, utiliza_ /help",
        parse_mode=telegram.ParseMode.MARKDOWN)
  elif 'en' in read_database(chat_id):       # 'en' because of "English"
    bot.sendMessage(chat_id,text="Hello "+name+", welcome 😄 \n\n*For downloading a song you can:*\nSend me the *NAME AND ARTIST 🎤*\n_THE SONG URL 🎶_\nUse /vid _FOR LOOKING FOR SONGS_ 🔍\n\nFor discovering _more about the bot, use_ /help",
      parse_mode=telegram.ParseMode.MARKDOWN)

@run_async
def lang(bot,update):                             # '/lang' handler function (disabled - it's only used when called by another function)
  print("\tEjecutando '/lang'...")
  user = update.message.from_user['first_name']
  chat_id = update.message.chat_id
  name = unidecode(user)
  print("Usuario + ID: ",name,chat_id)
  if read_database(chat_id) == None:
    key_l(bot,update)
  else:
    key_l2(bot,update)

@run_async
def pref(bot,update):                             # '/preferences' handler function, replacing the old '/lang' function with additional features
  print("\tEjecutando '/preferences'...")
  user = update.message.from_user['first_name']
  chat_id = update.message.chat_id
  name = unidecode(user)
  print("Usuario + ID: ",name,chat_id)
  if read_database(chat_id)==None:
    bot.sendMessage(chat_id,text="Antes de continuar, debes actualizar tus preferencias de idioma\n\nBefore you continue, you have to update your language preferences")
    lang(bot,update)
  elif 'es' in read_database(chat_id):
    key_pr(bot,update)                            # Different keyboards redirects to "language" function or "operative system" function
  elif 'en' in read_database(chat_id):
    key_pren(bot,update)                          # If a function name is like "key_pr" + en then it means "English" function (key_prEN)

@run_async
def help(bot,update):                             # '/help' handler function
  print("\tEjecutando '/help'...")
  user = update.message.from_user['first_name']
  chat_id=update.message.chat_id
  name = unidecode(user)
  print("Usuario + ID: ",name,chat_id)
  if read_database(chat_id)==None:           # Always check language preferences for avoiding message errors (no lang defined)
    bot.sendMessage(chat_id,text="Antes de continuar, debes actualizar tus preferencias de idioma\n\nBefore you continue, you have to update your language preferences")
    lang(bot,update)
  elif 'es' in read_database(chat_id):
    bot.sendMessage(chat_id,
      text="A continuación tienes la lista de comandos:\n\n - /vid, para aprender a *utilizar el bot* @vid para buscar vídeos 🔍\
      \n\n - /privacy, donde podrás conocer *las políticas de privacidad* 👮\n\n - /preferences, para cambiar *tus preferencias de idioma 🗣* o *sistema operativo ⚙* cuando quieras\
      \n\n - /errors, para *recibir asistencia* 🛠\n\n\
 - /changelog, orientado más a los _desarrolladores_ 🤓 pero abierto a todo el mundo: la *lista de cambios y mejoras* que se incluyen con cada actualización del bot y enlace al proyecto de GitHub\n\n\n\
*NOTA:* el Bot se desconecta a las _23:10_ (hora española) _para mantenimiento y actualización_ y vuleve a estar activo a las *9:30*.",
      parse_mode=telegram.ParseMode.MARKDOWN)
  elif 'en' in read_database(chat_id):
    bot.sendMessage(chat_id,
      text="Now you have command list:\n\n - /vid, for learning *how to use the bot* @vid for searching videos 🔍\
      \n\n - /privacy, where you can see *privacy policies* 👮\n\n - /preferences, for changing *your language preferences 🗣* or *operative system ones ⚙* whenever you want\
      \n\n - /errors, for *getting help* 🛠\n\n\
 - /changelog, designed for _developers_ 🤓 but accessible for everyone: list of *changes and improvements* included in each bot update and link to GitHub project\n\n\n\
*INFO:* The Bot turns off at _23:10_ (Spanish time zone) _for maintenance and updates_ and is available at *9:30*.",
      parse_mode=telegram.ParseMode.MARKDOWN)

@run_async
def nothing(bot,update):                          # 'nothing' function for unexpected messages (documents, contacts, etc)
  user = update.message.from_user['first_name']
  chat_id = update.message.chat_id
  name = unidecode(user)
  print("Usuario + ID: ",name,chat_id)
  if read_database(chat_id)==None:
    bot.sendMessage(chat_id,text="Antes de continuar, debes actualizar tus preferencias de idioma\n\nBefore you continue, you have to update your language preferences")
    lang(bot,update)
  elif 'es' in read_database(chat_id):
    bot.sendMessage(chat_id=update.message.chat_id,text="No puedo hacer nada con lo que me has enviado 🤔\n\nEscribe   /help   para obtener ayuda")
  elif 'en' in read_database(chat_id):
    bot.sendMessage(chat_id,text="I can not do anything with what you have sent me 🤔\n\nType  /help   to get help")

@run_async
def privacy(bot,update):                          # '/privacy' function
  print("\tEjecutando '/privacy'...")
  user = update.message.from_user['first_name']
  chat_id=update.message.chat_id
  name = unidecode(user)
  print("Usuario + ID: ",name,chat_id)
  if read_database(chat_id)==None:
    bot.sendMessage(chat_id,text="Antes de continuar, debes actualizar tus preferencias de idioma\n\nBefore you continue, you have to update your language preferences")
    lang(bot,update)
  elif 'es' in read_database(chat_id):
    bot.sendMessage(chat_id,
      text="@dwnmp3Bot únicamente guarda y conserva tu *nombre público* 🗣 y el *id del chat* 🆔 (requerido para enviar los archivos necesarios) junto con tus *preferencias de idioma* y de *sistema operativo* (para que no tengas que escribirlo cada vez). Finalmente, con fines méramente estadísticos, llevamos una cuenta con *la cantidad de descargas realizadas* ⤵\n\nGracias por confiar en nosotros 😃",
      parse_mode=telegram.ParseMode.MARKDOWN)
  elif 'en' in read_database(chat_id):
    bot.sendMessage(chat_id,
      text="@dwnmp3Bot is only saving your *public name* 🗣 and *chat id* 🆔 (requiered for sending files) with your *language preferences* and *operating system* ones (in order to not to make you writing them each time). Finally, with stadistical purposes, we count *how many downloads you have done* ⤵\n\nThanks for trusting us 😃",
      parse_mode=telegram.ParseMode.MARKDOWN)

@run_async
def errors(bot,update):                           # '/errors' function
  print("\tEjecutando '/errors'...")
  chat_id=update.message.chat_id
  user = update.message.from_user['first_name']
  name = unidecode(user)
  print("Usuario + ID: ",name,chat_id)
  if read_database(chat_id)==None:
    bot.sendMessage(chat_id,text="Antes de continuar, debes actualizar tus preferencias de idioma\n\nBefore you continue, you have to update your language preferences")
    lang(bot,update)
  elif 'es' in read_database(chat_id):
    mensaje_bot(bot,update,chat_id)
  elif 'en' in read_database(chat_id):
    message_bot(bot,update,chat_id)

@run_async
def vid(bot,update):                              # '/vid' function
  print("\tEjecutando '/vid'...")
  user = update.message.from_user['first_name']
  chat_id=update.message.chat_id
  name = unidecode(user)
  print("Usuario + ID: ",name,chat_id)
  if read_database(chat_id)==None:
    bot.sendMessage(chat_id,text="Antes de continuar, debes actualizar tus preferencias de idioma\n\nBefore you continue, you have to update your language preferences")
    lang(bot,update)
  elif 'es' in read_database(chat_id):
    bot.sendMessage(chat_id,"Voy a enseñarte a utilizar el bot @vid")
    time.sleep(3)
    step1 = open('/home/javier/BOT/paso1.png','rb')
    bot.sendPhoto(chat_id,step1)
    bot.sendMessage(chat_id,"Escribes en el teclado @vid para llamar al bot")
    time.sleep(7)
    step2 = open('/home/javier/BOT/paso2.png','rb')
    bot.sendPhoto(chat_id,step2)
    bot.sendMessage(chat_id,
      text="Empiezas a escribir el *título del vídeo* que quieras encontrar",
      parse_mode=telegram.ParseMode.MARKDOWN)
    time.sleep(7)
    step3 = open('/home/javier/BOT/paso3.png','rb')
    bot.sendPhoto(chat_id,step3)
    bot.sendMessage(chat_id,
      text="Una vez encuentres el vídeo que quieras descargar, *pulsas sobre él directamente*",
      parse_mode=telegram.ParseMode.MARKDOWN)
    time.sleep(7)
    step4 = open('/home/javier/BOT/paso4.png','rb')
    bot.sendPhoto(chat_id,step4)
    bot.sendMessage(chat_id,"Se enviará el vídeo seleccionado y comenzará la descarga automáticamente")
    time.sleep(3)
    final = open('/home/javier/BOT/paso5.png','rb')
    bot.sendPhoto(chat_id,final)
    bot.sendMessage(chat_id,"Listo, ya sabes cómo utilzar el bot @vid 😃")
  elif 'en' in read_database(chat_id):
    bot.sendMessage(chat_id,"I'm going to show you how to use the bot @vid")
    time.sleep(3)
    step1 = open('/home/javier/BOT/paso1.png','rb')
    bot.sendPhoto(chat_id,step1)
    bot.sendMessage(chat_id,"First, type *as a message* @vid to call the bot",
      parse_mode=telegram.ParseMode.MARKDOWN)
    time.sleep(7)
    step2 = open('/home/javier/BOT/paso2.png','rb')
    bot.sendPhoto(chat_id,step2)
    bot.sendMessage(chat_id,
      text="Then, *start typing the title* of the video you want to find",
      parse_mode=telegram.ParseMode.MARKDOWN)
    time.sleep(7)
    step3 = open('/home/javier/BOT/paso3.png','rb')
    bot.sendPhoto(chat_id,step3)
    bot.sendMessage(chat_id,
      text="When you see the video you want to download, *press on it directly*",
      parse_mode=telegram.ParseMode.MARKDOWN)
    time.sleep(7)
    step4 = open('/home/javier/BOT/paso4.png','rb')
    bot.sendPhoto(chat_id,step4)
    bot.sendMessage(chat_id,"The chosen video will be sent and the download will start")
    time.sleep(3)
    final = open('/home/javier/BOT/paso5.png','rb')
    bot.sendPhoto(chat_id,final)
    bot.sendMessage(chat_id,"It's done, now you know how to use the bot @vid 😃")

@run_async
def button(bot, update):                                # 'button' function
    query = update.callback_query                       # which gets 'callback_query' from "InlineKeyboard" buttons (if you press "Yes, continue", this functions detects it and sends to
    chat_id = query['message']['chat']['id']            # "botones" function for handling it
    name = query['message']['chat']['first_name']
    user = unidecode(name)
    print("\tUsuario: ",user)
    print("\tOpción elegida: ",query.data)
    value=query.data
    star="https://goo.gl/12AADY"
    name = "dur_{}.txt".format(chat_id)                 # Data is stored in .txt files (with this we avoid problems of 'None' in variables)
    title_file="title_{}.txt".format(chat_id)
    message_id = query.message.message_id
    botones(bot,update,chat_id,message_id,value,user)

@run_async
def changes(bot,update):                                # '/changelog' function
  user = update.message.from_user['first_name']
  chat_id = update.message.chat_id
  name = unidecode(user)
  print("\tEjecutando '/changelog'")
  print("Usuario + ID: ",name,chat_id)
  github = "https://github.com/Javinator9889/telegram-yt_mp3-bot"
  if read_database(chat_id)==None:
    bot.sendMessage(chat_id,text="Antes de continuar, debes actualizar tus preferencias de idioma\n\nBefore you continue, you have to update your language preferences")
    lang(bot,update)
  elif 'es' in read_database(chat_id):
    bot.sendMessage(chat_id=update.message.chat_id,
      text="*Versión actual:* _2.3.10.26.04_\n\n- *SOLUCIÓN DEFINITIVA A LAS DESCARGAS*\n\n- *TRADUCCIÓN COMPLETA A INGLÉS*: usa el comando /preferences para definir tu idioma.\n\n- Nueva duración máxima: *1 hora*.\
      \n- *METADATOS en todas las descargas*\n- Optimizada la velocidad *de descarga*.\n- Mejorados los *tiempos de espera*.\n- Optimización de los _servicios_ (debido a la nueva longitud máxima admitida).\
      \n- Tiempo de espera automático *si la congestión del servidor está por encima del 80%*.\n- Añadido *multiproceso* para atender hasta 50 peticiones simultáneas (en un futuro se _ampliará_).\
      \n- Solucionado un error por el cual *no se descargaban los vídeos*.\n- Nuevo mensaje cuando *un vídeo largo no puede ser enviado*.\
      \n- *Actualización del servidor*: descargas simultáneas sin errores ni fallos\
      \n- *Diálogos en la función* /errors: ahora, al escribir el comando /errors, interactúas con el bot para ofrecer la mejor asistencia.\
      \n- *Nuevo algoritmo de búsqueda*\n- Solucionado *un bug* por el cual _las descargas se bloqueaban_ y no comenzaban. Disculpad las molestias.\n- *Diálogos* optimizados\n- *Correcciones menores de errores*.\n\n*ACCEDE AL PROYECTO EN GitHub* [justo aquí]("+github+")",
      parse_mode=telegram.ParseMode.MARKDOWN)
  elif 'en' in read_database(chat_id):
    bot.sendMessage(chat_id=update.message.chat_id,
      text="*Current version:* _2.3.10.26.04_\n\n- *DEFINITIVE SOLUTION FOR DOWNLOADS*\n\n- *COMPLETE ENGLISH TRANSLATION*: use /preferences to define your language.\n\n- New maximum duration: *1 hour*.\
      \n- *METADATA in all downloads*\n- Optimized *download speed*.\n- Improved *waiting times*.\n- _Service_ optimizations (because of the new video lenght).\n- Automatic wait time *if server congestion is above 80%*.\
      \n- Added *multi-process* to handle up to 50 concurrent requests (in a future wil be extended)\n- Fixed an error by which *the videos were not downloaded*.\
      \n- New message when *a long video can not be sent*.\n- *Server update*: simultaneous downloads without errors or failures.\
      \n- *Dialogs in the function* /errors: now, when writing the /errors command, you will be able to interact with the bot to offer you the best support.\
      \n- Solved *a bug* which _locked downloads_ and made them not starting. Sorry for the inconvenience\n- *Optimized* dialogs\n- *New search algorithm*\n- *Minur bug fixes*\n\n*ACCESS TO GitHub PROJECT* [right here]("+github+")",
      parse_mode=telegram.ParseMode.MARKDOWN)

@run_async
def photo(bot,update):                                   # Function for handling photo-messages
  user = update.message.from_user['first_name']
  chat_id = update.message.chat_id
  name = unidecode(user)
  print("\tRecibida imagen")
  print("Usuario + ID: ",name,chat_id)
  if read_database(chat_id)==None:
    bot.sendMessage(chat_id,text="Antes de continuar, debes actualizar tus preferencias de idioma\n\nBefore you continue, you have to update your language preferences")
    lang(bot,update)
  elif 'es' in read_database(chat_id):
    bot.sendMessage(chat_id,text="*¡¡NO VEO!!* *¡¡ME HE QUEDADO CIEGO!!*\nAh, no... Que no tengo ojos 😅",
      parse_mode=telegram.ParseMode.MARKDOWN)
  elif 'en' in read_database(chat_id):
    bot.sendMessage(chat_id,text="*I CAN'T SEE ANYTHING!!* *I'M BLIND!!*\nAh, no... I have no eyes 😅",
      parse_mode=telegram.ParseMode.MARKDOWN)

@run_async
def song(bot,update):                                    # Function for handling audio-messages
  user = update.message.from_user['first_name']
  chat_id = update.message.chat_id
  name = unidecode(user)
  print("\tRecibida canción")
  print("Usuario + ID: ",name,chat_id)
  if read_database(chat_id)==None:
    bot.sendMessage(chat_id,text="Antes de continuar, debes actualizar tus preferencias de idioma\n\nBefore you continue, you have to update your language preferences")
    lang(bot,update)
  elif 'es' in read_database(chat_id):
    bot.sendMessage(chat_id,text="Tienes un gusto horrible... Mejor te envío yo algo 😜",
      parse_mode=telegram.ParseMode.MARKDOWN)
  elif 'en' in read_database(chat_id):
    bot.sendMessage(chat_id,text="You have a horrible taste in music... I better send you something 😜",
      parse_mode=telegram.ParseMode.MARKDOWN)

@run_async
def video(bot,update):                                   # Function for handling video-messages
  user = update.message.from_user['first_name']
  chat_id = update.message.chat_id
  name = unidecode(user)
  print("\tRecibido vídeo")
  print("Usuario + ID: ",name,chat_id)
  if read_database(chat_id)==None:
    bot.sendMessage(chat_id,text="Antes de continuar, debes actualizar tus preferencias de idioma\n\nBefore you continue, you have to update your language preferences")
    lang(bot,update)
  elif 'es' in read_database(chat_id):
    bot.sendMessage(chat_id,text="Gracias pero yo soy más de cine mudo escocés subtitulado en ruso 😶. Prueba a descargar algo",
      parse_mode=telegram.ParseMode.MARKDOWN)
  elif 'en' in read_database(chat_id):
    bot.sendMessage(chat_id,text="Thank you so much but I prefer Scottish silent movies with Russian subtitles 😶. Try to download something",
      parse_mode=telegram.ParseMode.MARKDOWN)

@run_async
def location(bot,update):                               # Function for handling location-messages
  user = update.message.from_user['first_name']
  chat_id = update.message.chat_id
  name = unidecode(user)
  print("\tRecibida ubicación")
  print("Usuario + ID: ",name,chat_id)
  if read_database(chat_id)==None:
    bot.sendMessage(chat_id,text="Antes de continuar, debes actualizar tus preferencias de idioma\n\nBefore you continue, you have to update your language preferences")
    lang(bot,update)
  elif 'es' in read_database(chat_id):
    bot.sendMessage(chat_id,text="ERROR 404\n\n¡¡NOS HAN DESCUBIERTO!! 🛰 INICIANDO PROTOCOLO DE AUTODESTRUCCIÓN...",
      parse_mode=telegram.ParseMode.MARKDOWN)
  elif 'en' in read_database(chat_id):
    bot.sendMessage(chat_id,text="ERROR 404\n\nWE HAVE BEEN DISCOVERED!! 🛰 STARTING SELF-DESTRUCTION PROTOCOL...",
      parse_mode=telegram.ParseMode.MARKDOWN)

@run_async
def voice(bot,update):                                  # Function for handling voice-messages
  user = update.message.from_user['first_name']
  chat_id = update.message.chat_id
  name = unidecode(user)
  print("\tRecibido audio")
  print("Usuario + ID: ",name,chat_id)
  if read_database(chat_id)==None:
    bot.sendMessage(chat_id,text="Antes de continuar, debes actualizar tus preferencias de idioma\n\nBefore you continue, you have to update your language preferences")
    lang(bot,update)
  elif 'es' in read_database(chat_id):
    bot.sendMessage(chat_id,text="Una voz preciosa, pero particularmente prefiero a _Lady GaGa_ 💃",
      parse_mode=telegram.ParseMode.MARKDOWN)
  elif 'en' in read_database(chat_id):
    bot.sendMessage(chat_id,text="What a beautiful voice, but I prefer _Lady GaGa_ 💃",
      parse_mode=telegram.ParseMode.MARKDOWN)

# Print in console the requierd Copyright message because of GLP v3 license

print("YouTube MP3 Downloader Bot (Telegram)  Copyright (C) 2017  Javinator9889\n\n\
This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.\n\
This is free software, and you are welcome to redistribute it\
under certain conditions; type `show c' for details.")

# Initialize main system variables
token = {}                                                    # Token dictionary
archivo_token = open("token.txt", "r")                        # Reads token from .txt file
token["Telegram"] = archivo_token.readline()
archivo_api = open("API_KEY.txt","r")                         # Reads YouTube API from .txt file
API=archivo_api.readline()

# Initialize Telegram-bot variables
updater = Updater(token["Telegram"], workers=50)              # Starts 50 threads for "updater" (declared with '@run_async' decorator)
dispatcher = updater.dispatcher                               # Starts "dispatcher" requierd to make the bot working properly

# Initialize "Command" handlers
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)
ayuda_handler = CommandHandler('help', help)
dispatcher.add_handler(ayuda_handler)
privacidad_handler = CommandHandler('privacy', privacy)
dispatcher.add_handler(privacidad_handler)
error_handler = CommandHandler('errors', errors)
dispatcher.add_handler(error_handler)
vid_handler = CommandHandler('vid', vid)
dispatcher.add_handler(vid_handler)
change_handler = CommandHandler('changelog', changes)
dispatcher.add_handler(change_handler)
pref_handler = CommandHandler('preferences', pref)
dispatcher.add_handler(pref_handler)

# Initialize "Message" handlers
photo_handler = MessageHandler(Filters.photo, photo)
dispatcher.add_handler(photo_handler)
video_handler = MessageHandler(Filters.video, video)
dispatcher.add_handler(video_handler)
song_handler = MessageHandler(Filters.audio, song)
dispatcher.add_handler(song_handler)
voice_handler = MessageHandler(Filters.voice, voice)
dispatcher.add_handler(voice_handler)
loc_handler = MessageHandler(Filters.location, location)
dispatcher.add_handler(loc_handler)
nothing_handler = MessageHandler((Filters.sticker | Filters.contact | Filters.document), nothing)
dispatcher.add_handler(nothing_handler)

# Initialize "button" 'CallbackQueryHandler' required for InlineKeyborads
updater.dispatcher.add_handler(CallbackQueryHandler(button))

# Starts "updater" in order to getting updates and messages from Telegram servers
updater.start_polling()

# Prints basic bot information as it is working and the current version
print("\nBot en funcionamiento")
print("\nVersión: 2.3.10.26.04")
try:
    while 1:
        time.sleep(10)    # Prevents the bot from disconnecting
except KeyboardInterrupt:
    updater.idle()        # Stops the bot only with "Ctrl+C" on keyboard
    print ("\nBot detenido\nFinalizando...")

# The next message has to be included in every copy of this program, modified or not
"""
    YouTube MP3 Downloader Bot (Telegram) -- A simple bot for downloading every YouTube video in MP3 format
    Copyright (C) 2017  Javinator9889

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    For contacting, go to "https://github.com/Javinator9889/telegram-yt_mp3-bot/issues" and type your message.
    Also you can go to my GitHub profile and send me direct message.
"""