import telegram
import os, sys                # Basic python libraries
import os.path as path        # Basic python libraries
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import time
from datetime import datetime # Basic python libraries
from errores import key_b,key_ed,key_o, key_eden, key_oen
from pafy_test import key_f, key_fen   # From file "pafy_test.py"
from sender import sender
from curl import descarga              # From file "curl.py"
from database import write_database,read_database,write_os,read_os

# This function is for distributing the "callback queries" between different options. Also it's for basic ReplyKeyboardMarkup

def key_l(bot, update,chat_id):
    keyboard = [[InlineKeyboardButton("Español 🇪🇸", callback_data='es'),InlineKeyboardButton("English 🇬🇧", callback_data='en')]]

    reply_markup2 = InlineKeyboardMarkup(keyboard)

    bot.sendMessage(text='Elige tu idioma / choose your language:',
      parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup2, chat_id=chat_id)


def key_l2(bot, update,chat_id):
    keyboard = [[InlineKeyboardButton("Español 🇪🇸", callback_data='castell'),InlineKeyboardButton("English 🇬🇧", callback_data='glish')]]

    reply_markup2 = InlineKeyboardMarkup(keyboard)

    bot.sendMessage(text='Elige tu idioma / choose your language:',
      parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup2, chat_id=chat_id)

def key_os(bot, update,chat_id):
    keyboard = [[InlineKeyboardButton("Android - W. Phone 🇦", callback_data='droid'),InlineKeyboardButton("iOS 🇮", callback_data='ios')]]

    reply_markup2 = InlineKeyboardMarkup(keyboard)

    bot.sendMessage(text='¿Cuál es tu sistema operativo? _(solo móviles; en PC es irrelevante)_',
      parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup2,chat_id=chat_id)

def key_osen(bot, update,chat_id):
    keyboard = [[InlineKeyboardButton("Android - W. Phone 🇦", callback_data='droiden'),InlineKeyboardButton("iOS 🇮", callback_data='iosen')]]

    reply_markup2 = InlineKeyboardMarkup(keyboard)

    bot.sendMessage(text='What is your operative system? _(only smartphones; this option is irrelevant for PC users)_',
      parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup2,chat_id=chat_id)

def botones(bot,update,chat_id,message_id,value,user):  # 'value' is obtained from "def buttons" in 'TeleBotSongDownloader.py'
    title_file="title_{}.txt".format(chat_id)
    video_file = "url_{}.txt".format(chat_id)
    if path.exists(title_file):
      file=open(title_file,'r')
      title = file.readline()
      full_name="{}_{}.mp3".format(title,chat_id)
      file.close()
    star="https://goo.gl/12AADY"
    hour_spain = "http://24timezones.com/es_husohorario/madrid_hora_actual.php"
    hour_eng = "http://24timezones.com/world_directory/time_in_madrid.php"
    if value =="1":
      if 'es' in read_database(chat_id):
        bot.editMessageText(text="Prueba a intentar la descarga de nuevo.\n\nPrueba a introducir la URL del vídeo directamente (suele funcionar en la mayoría de los casos).\n\nDisculpa las molestias. *Si necesitas más ayuda*, escribe  /errors",
                        chat_id=chat_id,
                        message_id=message_id,
                        parse_mode=telegram.ParseMode.MARKDOWN)
      elif 'en' in read_database(chat_id):
        bot.editMessageText(text="Retry the download.\n\nTry to put the video URL directly (it usually works in almos cases).\n\nSorry for the inconvenience. *If you need more help*, type  /errors",
                        chat_id=chat_id,
                        message_id=message_id,
                        parse_mode=telegram.ParseMode.MARKDOWN)
    elif value =="2":
      if 'es' in read_database(chat_id):
        bot.editMessageText(text="Muchas gracias por utilizarme 😄\n\n\nPara descargar otra canción, puedes: \n\nescribirme directamente el *título* 🎵,\nmandar la *URL* del vídeo 📎,\n*buscar* el vídeo con  @vid ▶,\n/help _para más ayuda_\n\n*¿Te gusta este bot?* 👍 No dudes en enviarme tus comentarios [haciendo clic aquí]("+star+")",
                        parse_mode=telegram.ParseMode.MARKDOWN,
                        chat_id=chat_id,
                        message_id=message_id)
      elif 'en' in read_database(chat_id):
        bot.editMessageText(text="Thank you so much for using me 😄\n\n\nTo download another song, you can: \n\nsend me directly *the title of the video* 🎵,\nsend me *the URL of the video* 📎,\n*search the video* with @vid ▶,\n/help _for get assistance_\n\n*Do you like this bot?* 👍 Please send me your opinions [by clicking here]("+star+")",
                        parse_mode=telegram.ParseMode.MARKDOWN,
                        chat_id=chat_id,
                        message_id=message_id)

    elif value == "Ax":
      if 'es' in read_database(chat_id):
          bot.editMessageText(text="_Comenzando la descarga..._",
                        parse_mode=telegram.ParseMode.MARKDOWN,
                        chat_id=chat_id,
                        message_id=message_id)
      elif 'en' in read_database(chat_id):
          bot.editMessageText(text="_Starting download..._",
                        parse_mode=telegram.ParseMode.MARKDOWN,
                        chat_id=chat_id,
                        message_id=message_id)
      sender(bot,update,chat_id,user)
    elif value == "Ay":
      if 'es' in read_database(chat_id):
        bot.editMessageText(text="*Descarga cancelada*",
                        parse_mode=telegram.ParseMode.MARKDOWN,
                        chat_id=chat_id,
                        message_id=message_id)
      elif 'en' in read_database(chat_id):
        bot.editMessageText(text="*Download cancelled*",
                        parse_mode=telegram.ParseMode.MARKDOWN,
                        chat_id=chat_id,
                        message_id=message_id)
      if path.exists(title_file):
        os.remove(title_file)
      if path.exists(video_file):
        os.remove(video_file)
    elif value == "en":
      bot.editMessageText(text="_Preferences updated correctly..._\n\nIf you want to *change your language*, just use the command /preferences\n\n_If you were trying to download a video, please start again._",
                        parse_mode=telegram.ParseMode.MARKDOWN,
                        chat_id=chat_id,
                        message_id=message_id)
      data = None
      write_database(user,chat_id,value,data)
    elif value == "es":
      bot.editMessageText(text="_Preferencias actualizadas correctamente..._\n\nPara *cambiar el idioma en cualquier momento*, ejecuta /preferences\n\n_Si estabas intentando descargar un vídeo, por favor comienza de nuevo._",
                        parse_mode=telegram.ParseMode.MARKDOWN,
                        chat_id=chat_id,
                        message_id=message_id)
      data = None
      write_database(user,chat_id,value,data)
    elif value == "glish":
      bot.editMessageText(text="_Preferences updated correctly..._\n\nIf you want to *change your language*, just use the command /preferences",
                        parse_mode=telegram.ParseMode.MARKDOWN,
                        chat_id=chat_id,
                        message_id=message_id)
      value="en"
      data = "Something"
      write_database(user,chat_id,value,data)
    elif value == "castell":
      bot.editMessageText(text="_Preferencias actualizadas correctamente..._\n\nPara *cambiar el idioma en cualquier momento*, ejecuta /preferences",
                        parse_mode=telegram.ParseMode.MARKDOWN,
                        chat_id=chat_id,
                        message_id=message_id)
      value = "es"
      data = "Something"
      write_database(user,chat_id,value,data)
    elif value == "Ed":
      key_ed(bot,update,chat_id)
    elif value == "O":
      key_o(bot,update,chat_id)
    elif value == "V":
      bot.sendMessage(chat_id,text="Algunas veces, el servidor *sufre un colapso* 😫 y no se envían correctamente las canciones.\
        \n\nEsto se soluciona volviendo a pedirle al servidor que _descargue la canción_",
        parse_mode=telegram.ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardRemove())
    elif value == "U":
      bot.sendMessage(chat_id,text="Cuando el vídeo no puede ser obtenido _directamente desde Telegram_ (a causa del servidor de descargas), \
se manda un *enlace* 📎 para descargarlo y luego ya se puede conseguir directamente desde Telegram",
        parse_mode=telegram.ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardRemove())
    elif value == "Z":
      bot.sendMessage(chat_id,text="Antes de nada, ten en cuenta que *el bot se desconecta a las 23:10 🕚 (hora española)* \
y se reactiva a las *9:30* 🕤\n(visita [este enlace]("+hour_spain+") para saber la hora en España).\
        \n\nSi lo anterior no era tu caso, el bot puede no mostrar respuesta debido a un error ⚠ que no tenemos registrado. \
Todos los días revisamos los errores del bot, por lo que debería solucionarse en esta semana 😄",
        parse_mode=telegram.ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardRemove())
    elif value == "S":
      bot.sendMessage(chat_id,text="Cuando se produce una descarga muy lenta, entran en juego varios factores fundamentales:\
        \n\n*Tu ubicación* 🛰 es determinante, pues cuanto más lejos te encuentres del servidor más se tarda.\
        \n*Los usuarios activos* 👨‍👩‍👧‍👦 provocan una demora en los tiempos de descarga.\n*El servidor puede haberse bloqueado* 🌁.\
        \n*El servidor de descargas* ❌ no responde, siendo esta última la razón más usual para descargas lentas.\
        \n\nSin poder decir mucho más, *paciencia*: tarde o temprano la canción se acaba enviando y sino, pondremos medios para ello 😄",
        parse_mode=telegram.ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardRemove())
    elif value == "LK":
      bot.sendMessage(chat_id,text="Es posible que seas el descubridor de *un fallo nuevo* (weeh 😱👏🎉‼),\
 por lo que si quieres comentarlo ve a [este enlace]("+star+"), puntúa el bot ⭐ y a continuación, *deja una reseña* 📝.\nLas leemos _todos los días_, por lo que agradeceremos mucho tu aportación.",
        parse_mode=telegram.ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardRemove())
    elif value == "fi":
      bot.sendMessage(chat_id,text="Algunas veces, introduciendo *solo el nombre de la canción* 🎤 o *solo el artista* 💃 no es suficiente para el bot para encontrar *la canción que quieres*.\
        \n\nPara ello, te recomendamos que *ejecutes* /vid *para obtener una canción concreta* desde Telegram.",
        parse_mode=telegram.ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardRemove())
    elif value == "mn":
      bot.sendMessage(chat_id,text="_A continuación se muestran todos los errores registrados más comunes:_\n\n\n \"El bot manda un mensaje diciendo que *no se puede descargar* pero me manda un link para hacerlo\"\n\nEsto se produce en la mayoría de los casos debido a que la *página de descargas todavía no tiene la información que necesita Telegram para poder descargar el vídeo directamente*.\nUna vez lo descargas desde la página web, se suele _poder descargar desde el bot_.\n\n \"El bot dice que *no se ha encontrado nada*\"\n\nEsto se suele producir porque o bien *solo has introducido el nombre del artista* o porque *el vídeo no existe*. Prueba a utilizar el Bot   @vid    para _mandar directamente la URL del vídeo que quieras obtener_. (escribe   /vid    para más información).\n\n\"El archivo de audio tiene una parte que pone un número del estilo: _\"1234567\"_\"\n\nEl archivo que se envía tiene una ID asociada a cada usuario pues así no se extravía por el camino o produce algún fallo en el servidor.\nEstamos trabajando en una solución posible.\n\n\"El bot *tarda mucho en descargar* algunas canciones\"\n\nCuando ocurre esto, puede ser o bien porque nuestro servidor está *colapsado con solicitudes* o porque la plataforma que utilizamos para descargar el vídeo *no responde o tiene que atender demasiadas peticiones*. No hay solución posible más que esperar a que se envíe la canción o, en su defecto, un enlace para descargarla.",
        parse_mode=telegram.ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardRemove())
    elif value == "Eden":
      key_eden(bot,update,chat_id)
    elif value == "Oen":
      key_oen(bot,update,chat_id)
    elif value == "Ven":
      bot.sendMessage(chat_id,text="Sometimes the server *collapses* 😫 and the songs are not sent correctly.\
        \n\nThis is resolved by asking the server again to _download the song_",
        parse_mode=telegram.ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardRemove())
    elif value == "Uen":
      bot.sendMessage(chat_id,text="When a video can't be obtained _directly from Telegram_ (because of the download server), \
we provide you *a link* 📎 for downloading and then you can get it directly from Telegram",
        parse_mode=telegram.ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardRemove())
    elif value == "Zen":
      bot.sendMessage(chat_id,text="Before going to the possible solutions, keep in mind that *the bot turns off at 23:10 🕚 (Spanish time zone)* \
and starts at *9:30* 🕤\n(visit [this link]("+hour_eng+") to know the time in Spain).\
        \n\nIf your error wasn't because of that, the bot can be not able to show response because of a non-registered error ⚠. \
We check everyday the information about happened errors and it should be solved in this week 😄",
        parse_mode=telegram.ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardRemove())
    elif value == "Sen":
      bot.sendMessage(chat_id,text="When a very slow download is happening, some key factors are relevant:\
        \n\n*Your location* 🛰 is determinant, as when far away you are from the server and it takes longer to send you the song.\
        \n*Active users* 👨‍👩‍👧‍👦 can cause a delay in download-times.\n*Server can have got frozen* 🌁.\n*Download server* is not responding ❌, being this the most usual reason why downloads perform slowly.\
        \n\nI can only tell you *patience*: sooner or later your song will be availabe to download from Telegram by a way or other 😄",
        parse_mode=telegram.ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardRemove())
    elif value == "LKen":
      bot.sendMessage(chat_id,text="It's possible that you are the discoverer of a *new error* (weeh 😱👏🎉‼), so if you would like us to get known about it go to [this link]("+star+"), \
rate the bot ⭐ an then *leave a review* 📝.\nWe read them _every day_, so we will appreciate so much your contribution.",
        parse_mode=telegram.ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardRemove())
    elif value == "fien":
      bot.sendMessage(chat_id,text="Sometimes, giving the bot *only the name of the song* 🎤 or *only the artist* 💃 is not enough to find *the song you are looking for*.\
\n\nFor this, we recommend you *to execute* /vid *in order to get a specific song* directly from Telegram.",
        parse_mode=telegram.ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardRemove())
    elif value == "mnen":
      bot.sendMessage(chat_id,text="_Now we are displaying all registered common-errors:_\n\n\n \"The bot sends a message telling that *is not possible to download the song* but sends me a link to do it\"\n\nThis happens because *the download page we use still not have the information needed by Telegram to download the video directly*.\nOnce you have downloaded it from the web page, you can usually _download it from the bot_.\n\n \"The bot says that *nothing was found*\"\n\nThis usually happens because or *you have only send the artist name* or because *the video doesn't exist*. Try to use the bot  @vid  to _send the video URL directly_ (type  /vid  to learn how to use this bot).\n\n\"The audio file has a numbered part like: _\"1234567\"_\"\n\nThe audio file the bot sends you has your ID attached in order to send it only to you.\nWe are working on a possible solution.\n\n\"It takes a long time for the bot to download songs\"\n\nWhen this occur, can be becauseour server is *collapsed* or most probably because the *download platform* we are using is down. There is no possible solution more than waiting for the video to be downloaded.",
        parse_mode=telegram.ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardRemove())
    elif value == "3":
      bot.editMessageText(text="Por favor, espere...",
        chat_id=chat_id,
        message_id=message_id)
      url_file = descarga(chat_id,title)
      bot.sendMessage(text="Para los usuarios de dispositivos iOS 📱 (iPhone - iPad), aquí tenéis un enlace de [descarga directa]("+url_file+") (_recomendamos utilizar un explorador alternativo a Safari pues sino no se podrán guardar las descargas_. Prueba con *Dolphin Browser*",
        chat_id=chat_id,
        parse_mode=telegram.ParseMode.MARKDOWN)
      value="iOS"
      write_os(chat_id,user,value)
      os.remove(full_name)
      try:
        if path.exists(down_file):
          os.remove(down_file)
        if path.exists(title_file):
          os.remove(title_file)
        if path.exists(down_file_2):
          os.remove(down_file_2)
        key_f(bot,update,chat_id)
      except PermissionError:
        key_f(bot,update,chat_id)
    elif value == "5":
      bot.editMessageText(text="Please, wait...",
        chat_id=chat_id,
        message_id=message_id)
      url_file = descarga(chat_id,title)
      bot.sendMessage(text="For iOS users 📱 (iPhone - iPad), here you have [a direct download link]("+url_file+") (_we recommend to use an alternative browser to Safari in order to save your song_. Try with *Dolphin Browser*",
        chat_id=chat_id,
        parse_mode=telegram.ParseMode.MARKDOWN)
      value="iOS"
      write_os(chat_id,user,value)
      os.remove(full_name)
      try:
        if path.exists(title_file):
          os.remove(title_file)
        key_fen(bot,update,chat_id)
      except PermissionError:
        key_fen(bot,update,chat_id)
    elif value == "4":
      bot.editMessageText(text="Perfecto, muchas gracias por tu colaboración (era solo para ayudar a los usuarios de iOS con la descarga)",
        chat_id=chat_id,
        message_id=message_id,
        parse_mode=telegram.ParseMode.MARKDOWN)
      value="Android"
      write_os(chat_id,user,value)
      os.remove(full_name)
      try:
        if path.exists(title_file):
          os.remove(title_file)
        key_f(bot,update,chat_id)
      except PermissionError:
        key_f(bot,update,chat_id)
    elif value == "6":
      bot.editMessageText(text="Perfect, thank you so much for your colaboration (that was only for helping iOS users with the download)",
        chat_id=chat_id,
        message_id=message_id,
        parse_mode=telegram.ParseMode.MARKDOWN)
      value="Android"
      write_os(chat_id,user,value)
      os.remove(full_name)
      try:
        if path.exists(title_file):
          os.remove(title_file)
        key_fen(bot,update,chat_id)
      except PermissionError:
        key_fen(bot,update,chat_id)
    elif value == "lang":
      bot.editMessageText(text="Actualizando preferencias de idioma...",
        chat_id=chat_id,
        message_id=message_id)
      key_l(bot,update,chat_id)
    elif value == "langen":
      bot.editMessageText(text="Updating language preferences...",
        chat_id=chat_id,
        message_id=message_id)
      key_l2(bot,update,chat_id)
    elif value == "os":
      bot.editMessageText(text="Actualizando preferencias de sistema operativo...",
        chat_id=chat_id,
        message_id=message_id)
      key_os(bot,update,chat_id)
    elif value == "osen":
      bot.editMessageText(text="Updating operative system preferences...",
        chat_id=chat_id,
        message_id=message_id)
      key_osen(bot,update,chat_id)
    elif value == "droid":
      bot.editMessageText(text="Preferencias actualizadas correctamente...\n\nUsa /preferences para cambiarlas en cualquier momento",
        chat_id=chat_id,
        message_id=message_id)
      value="Android"
      write_os(chat_id,user,value)
    elif value == "droiden":
      bot.editMessageText(text="Preferences updated correctly...\n\nUse /preferences for changing them whenever you want",
        chat_id=chat_id,
        message_id=message_id)
      value="Android"
      write_os(chat_id,user,value)
    elif value == "ios":
      bot.editMessageText(text="Preferencias actualizadas correctamente...\n\nUsa /preferences para cambiarlas en cualquier momento",
        chat_id=chat_id,
        message_id=message_id)
      value="iOS"
      write_os(chat_id,user,value)
    elif value == "iosen":
      bot.editMessageText(text="Preferences updated correctly...\n\nUse /preferences for changing them whenever you want",
        chat_id=chat_id,
        message_id=message_id)
      value="iOS"
      write_os(chat_id,user,value)