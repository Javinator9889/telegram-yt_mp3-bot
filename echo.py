from urllib.request import urlopen     # urllib2/3 in python3 is now inside 'urllib.request'
import ujson as json                   # pip install ujson (Visual C++ 14 Redistributable required)
import os, sys
import os.path as path
import telegram
import time
import urllib.request                  # We use this module for downloading from URLs
import isodate                         # Get video-length in ISO format and for converting to seconds
import unicodedata
from unidecode import unidecode
from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import re                              # For getting URLs from messages
from getVidId import getVidId          # From file "getVidId.py"
from getVidTitle import getVidTitle    # From file "getVidTitle.py"
from sender import sender              # From file "sender.py"
from botones import botones            # From file "botones.py"
from database import read_database,write_database   # From file "database.py"
from get_Vid_Id import get_yt_video_id # From file "get_Vid_Id.py"

# This function (echo) gets text from user and decides if it's an URL of YouTube or name and artist

@run_async
def key_a(bot, update):
    keyboard = [[InlineKeyboardButton("Continuar la descarga", callback_data='Ax'),InlineKeyboardButton("Cancelar", callback_data='Ay')]]

    reply_markup2 = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('¿Continuar con la descarga?',
      parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup2)
@run_async
def key_aen(bot,update):
    keyboard = [[InlineKeyboardButton("Continue download", callback_data='Ax'),InlineKeyboardButton("Cancell", callback_data='Ay')]]

    reply_markup2 = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Do you want to continue with the download?',
      parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup2)

@run_async
def key_l(bot, update):
    keyboard = [[InlineKeyboardButton("Español 🇪🇸", callback_data='es'),InlineKeyboardButton("English 🇬🇧", callback_data='en')]]

    reply_markup2 = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Elige tu idioma / choose your language:',
      parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup2)

@run_async
def echo(bot,update):
  texto1 = update.message['text']
  chat_id=update.message.chat_id
  message_id = update.message.message_id
  name = update.message.from_user['first_name']
  user = unidecode(name)
  command=unidecode(texto1)
  print("\n\tTexto recibido: ",command)
  if read_database(chat_id)==None:
    bot.sendMessage(chat_id,text="Antes de continuar, debes actualizar tus preferencias de idioma\n\nBefore you continue, you have to update your language preferences")
    key_l(bot,update)
  elif command == 'Al descargar':     # This checks if the message was from keyboards in function 'errores.py' and assigns a value for redirecting them to 'botones.py'
    value = 'Ed'
    print(value)
    botones(bot,update,chat_id,message_id,value,user)
  elif command == "Otro...":
    value = 'O'
    print(value)
    botones(bot,update,chat_id,message_id,value,user)
  elif command == "Archivo vacio (0.00 Bytes)":
    value = 'V'
    print(value)
    botones(bot,update,chat_id,message_id,value,user)
  elif command == "El video no puede ser obtenido":
    value = 'U'
    print(value)
    botones(bot,update,chat_id,message_id,value,user)
  elif command == "Descarga muy lenta":
    value = 'S'
    print(value)
    botones(bot,update,chat_id,message_id,value,user)
  elif command == "Error al buscar la cancion":
    value = 'fi'
    print(value)
    botones(bot,update,chat_id,message_id,value,user)
  elif command == "Mostrar todos los errores":
    value = 'mn'
    print(value)
    botones(bot,update,chat_id,message_id,value,user)
  elif command == "Otro error no registrado":
    value = 'LK'
    print(value)
    botones(bot,update,chat_id,message_id,value,user)
  elif command == "El bot no hace nada":
    value = 'Z'
    print(value)
    botones(bot,update,chat_id,message_id,value,user)
  elif command == "While downloading":
    value = 'Eden'
    print(value)
    botones(bot,update,chat_id,message_id,value,user)
  elif command == "Other...":
    value = 'Oen'
    print(value)
    botones(bot,update,chat_id,message_id,value,user)
  elif command == "Empty file (0.00 Bytes)":
    value = 'Ven'
    print(value)
    botones(bot,update,chat_id,message_id,value,user)
  elif command == "Video can't be downloaded":
    value = 'Uen'
    print(value)
    botones(bot,update,chat_id,message_id,value,user)
  elif command == "Downloading very slowly":
    value = 'Sen'
    print(value)
    botones(bot,update,chat_id,message_id,value,user)
  elif command == "Error while searching the song":
    value = 'fien'
    print(value)
    botones(bot,update,chat_id,message_id,value,user)
  elif command == "Show all registered errors":
    value = 'mnen'
    print(value)
    botones(bot,update,chat_id,message_id,value,user)
  elif command == "Another error not registered":
    value = 'LKen'
    print(value)
    botones(bot,update,chat_id,message_id,value,user)
  elif command == "The bot is not responding":
    value = 'Zen'
    print(value)
    botones(bot,update,chat_id,message_id,value,user)
  elif 'es' in read_database(chat_id):
      print("\n-----------------------------------------------------------------------------------------------------------------")
      print ("Debug [1]")
      print("-----------------------------------------------------------------------------------------------------------------")
      try:
        query0 = re.search("(?P<url>https?://[^\s]+)", command).group("url")    # It gets the first URL from message (if exists. Else, raises "AtributteError")
        Id=get_yt_video_id(query0)
        try:
          print("\tEjecutando descarga directa...")
          print("\tID: ",Id)
          if(Id == None):
            raise IndexError('El enlace proporcionado no tiene un formato conocido, o no contiene el ID del vídeo, o no es un enlace de YouTube')
          else:
            stndr_yt="http://youtube.com/watch?v="
            title1=getVidTitle(Id,chat_id,bot,update)
            title_file="title_{}.txt".format(chat_id)
            video_file = "url_{}.txt".format(chat_id)
            url2="https://www.googleapis.com/youtube/v3/videos?id={}&part=contentDetails&key=AIzaSyBUIuhTA4yUbC5dJr-mSr8Wcvirps34pcM".format(Id)
            print("\tURL API (2): ",url2)
            datas=urlopen(url2).read()
            json_data2=json.loads(datas)
            length=json_data2["items"][0]['contentDetails']['duration']
            print("\tDuración (ISO): ",length)
            dur=isodate.parse_duration(length)
            print("\tDuración: ",dur)
            durS=dur.total_seconds()
            print("\tDuración en segundos: ",durS)
            file = open(video_file,'w')
            yt_url="https://youtube.com/watch?v={}".format(Id)
            file.write(yt_url)
            file.close()
            file = open(title_file,'w')
            file.write(title1)
            file.close()
            if(durS>=3900):
              bot.sendMessage(chat_id,"La duración de la canción/vídeo elegido es demasiado larga (más de 60 minutos). La descarga se cancela")
              if path.exists(video_file):
                os.remove(video_file)
              if path.exists(title_file):
                os.remove(title_file)
            else:
              bot.sendMessage(chat_id,text="_Comenzando la descarga..._",parse_mode=telegram.ParseMode.MARKDOWN)
              time.sleep(1)
              sender(bot,update,chat_id,user)
        except IndexError:
            print("<<<<< IndexError al obtener información sobre el enlace (no existente) >>>>>")
            bot.sendMessage(chat_id,text="El enlace que nos has proporcionado no se corresponde con ningún vídeo.\n\nRevisa que está escrito correctamente o utiliza el bot @vid para buscar el vídeo (escribe /vid para saber cómo utilizarlo)")
      except AttributeError:      # The message is not containing an URL. So it's simple text message (query = command)
        query = command
        try:
              print("\tEjecutando búsqueda...")
              Id=getVidId(query,chat_id,bot,update)
              url2="https://www.googleapis.com/youtube/v3/videos?id={}&part=contentDetails&key=AIzaSyBUIuhTA4yUbC5dJr-mSr8Wcvirps34pcM".format(Id)
              url_title="https://www.googleapis.com/youtube/v3/videos?id={}&part=snippet&key=AIzaSyBUIuhTA4yUbC5dJr-mSr8Wcvirps34pcM".format(Id)
              print("\tURL de la api: ",url2)
              datas=urlopen(url2).read()
              json_data2=json.loads(datas)
              length=json_data2["items"][0]['contentDetails']['duration']
              data_t = urlopen(url_title).read()
              json_title = json.loads(data_t)
              title = json_title["items"][0]["snippet"]["title"]
              print("\tDuración (ISO): ",length)
              dur=isodate.parse_duration(length)
              print("\tDuración: ",dur)
              durS=dur.total_seconds()
              print("\tDuración en segundos: ",durS)
              if(durS>=3900):
                bot.sendMessage(chat_id,"Aquí tienes la URL del vídeo encontrado: http://youtube.com/watch?v="+Id+"")
                bot.sendMessage(chat_id,"La duración del vídeo es demasiado larga (más de 60 minutos).\n\nLa descarga se cancela")
              else:
                title_prev = title.translate({ord(c): None for c in '.:",/\!@#$'})
                title1 = title_prev.translate({ord('á'): 'a', ord('é'): 'e',ord('í'): 'i',ord('ó'): 'o',ord('ú'): 'u',ord('ñ'): 'n'})
                title_file="title_{}.txt".format(chat_id)
                video_file = "url_{}.txt".format(chat_id)
                file = open(title_file,'w')
                file.write(title1)
                file.close()
                file = open(video_file,'w')
                yt_url="https://youtube.com/watch?v={}".format(Id)
                file.write(yt_url)
                file.close()
                bot.sendMessage(chat_id,"La canción encontrada es esta: http://youtube.com/watch?v="+Id+" ")
                key_a(bot,update)
        except ValueError:
              print("\n\t<<<<<< Error al buscar el vídeo (no encontrado) | ID: ",chat_id,">>>>>>\n")
              bot.sendMessage(chat_id,"No hemos encontrado ninguna canción en base a los términos de búsqueda especificados.\n\nPrueba a escribir sin tildes o busca tu vídeo con   @vid   directamente desde el teclado")
        except IndexError:
              print("\n<<<<<<\"IndexError\" heredado de la función anterior (getVidId) | ID: ",chat_id,">>>>>>\n")  # When IndexError is raised in 'getVidId', main function raises too. So as for this, we set it to "IndexError inherited from getVidId"
  elif 'en' in read_database(chat_id):
      print("\n-----------------------------------------------------------------------------------------------------------------")
      print ("Debug [1]")
      print("-----------------------------------------------------------------------------------------------------------------")
      try:
        query0 = re.search("(?P<url>https?://[^\s]+)", command).group("url")    # As the bot is multi-langauge, two functions are needed
        Id=get_yt_video_id(query0)
        try:
          print("\tEjecutando descarga directa...")
          print("\tID: ",Id)
          if(Id == None):
            raise IndexError('El enlace proporcionado no tiene un formato conocido, o no contiene el ID del vídeo, o no es un enlace de YouTube')
          else:
            stndr_yt="http://youtube.com/watch?v="
            title1=getVidTitle(Id,chat_id,bot,update)
            url2="https://www.googleapis.com/youtube/v3/videos?id={}&part=contentDetails&key=AIzaSyBUIuhTA4yUbC5dJr-mSr8Wcvirps34pcM".format(Id)
            print("\tURL API (2): ",url2)
            datas=urlopen(url2).read()
            json_data2=json.loads(datas)
            length=json_data2["items"][0]['contentDetails']['duration']
            print("\tDuración (ISO): ",length)
            dur=isodate.parse_duration(length)
            print("\tDuración: ",dur)
            durS=dur.total_seconds()
            print("\tDuración en segundos: ",durS)
            title_file="title_{}.txt".format(chat_id)
            video_file = "url_{}.txt".format(chat_id)
            file = open(title_file,'w')
            file.write(title1)
            file.close()
            file = open(video_file,'w')
            yt_url="https://youtube.com/watch?v={}".format(Id)
            file.write(yt_url)
            file.close()
            if(durS>=3900):
              bot.sendMessage(chat_id,"Video lenght is too long (more than 60 minutes). Download cancelled")
              if path.exists(video_file):
                  os.remove(video_file)
              if path.exists(title_file):
                  os.remove(title_file)
            else:
                bot.sendMessage(chat_id,text="_Starting download..._",parse_mode=telegram.ParseMode.MARKDOWN)
                time.sleep(1)
                sender(bot,update,chat_id,user)
        except IndexError:
            print("<<<<< IndexError al obtener información sobre el enlace (no existente) >>>>>")
            bot.sendMessage(chat_id,text="The link you provided does not refer to any videos.\n\nCheck if it's writed correctly or use the bot @vid to search the video (type /vid to learn how to use it)")
      except AttributeError:
        query = command
        try:
              print("\tEjecutando búsqueda...")
              Id=getVidId(query,chat_id,bot,update)
              url2="https://www.googleapis.com/youtube/v3/videos?id={}&part=contentDetails&key=AIzaSyBUIuhTA4yUbC5dJr-mSr8Wcvirps34pcM".format(Id)
              url_title="https://www.googleapis.com/youtube/v3/videos?id={}&part=snippet&key=AIzaSyBUIuhTA4yUbC5dJr-mSr8Wcvirps34pcM".format(Id)
              print("\tURL de la api: ",url2)
              datas=urlopen(url2).read()
              json_data2=json.loads(datas)
              length=json_data2["items"][0]['contentDetails']['duration']
              data_t = urlopen(url_title).read()
              json_title = json.loads(data_t)
              title = json_title["items"][0]["snippet"]["title"]
              print("\tDuración (ISO): ",length)
              dur=isodate.parse_duration(length)
              print("\tDuración: ",dur)
              durS=dur.total_seconds()
              print("\tDuración en segundos: ",durS)
              if(durS>=3900):
                bot.sendMessage(chat_id,"Here is the URL of the video found: http://youtube.com/watch?v="+Id+"")
                bot.sendMessage(chat_id,"Video lenght is too long (more than 60 minutes). Download cancelled")
              else:
                title_prev = title.translate({ord(c): None for c in '.:",/\!@#$'})
                title1 = title_prev.translate({ord('á'): 'a', ord('é'): 'e',ord('í'): 'i',ord('ó'): 'o',ord('ú'): 'u',ord('ñ'): 'n'})
                title_def=unidecode(title1)
                title_file="title_{}.txt".format(chat_id)
                video_file = "url_{}.txt".format(chat_id)
                file = open(title_file,'w')
                file.write(title_def)
                file.close()
                file = open(video_file,'w')
                yt_url="https://youtube.com/watch?v={}".format(Id)
                file.write(yt_url)
                file.close()
                bot.sendMessage(chat_id,"The found song is this: http://youtube.com/watch?v="+Id+" ")
                key_aen(bot,update)
        except ValueError:
              print("\n\t<<<<<< Error al buscar el vídeo (no encontrado) | ID: ",chat_id,">>>>>>\n")
              bot.sendMessage(chat_id,"We did not find any songs based on the specified search terms.\n\nTry typing without titles or searching your video with  @vid  directly from the keyboard")
        except IndexError:
              print("\n<<<<<<\"IndexError\" heredado de la función anterior (getVidId) | ID: ",chat_id,">>>>>>\n")

archivo_api = open("API_KEY.txt","r")
API=archivo_api.readline()