from urllib.request import urlopen
import urllib.error
import ujson as json
import unicodedata
from unidecode import unidecode
from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

def getVidTitle(query,chat_id,bot,update):
  try:
    print("\n----------------------------------------------------------------------------------------------------------------------------")
    print("Debug [2.5]")
    print("----------------------------------------------------------------------------------------------------------------------------")
    Id = query
    url="https://www.googleapis.com/youtube/v3/videos?id={}&part=snippet&key={}".format(Id,API)
    print ("\tEnlace de la API (2): ",url)
    content=urlopen(url)
    json_text=content.read()
    data=json.loads(json_text)
    contenido=data["items"]
    if(contenido==[]):
      title_def="Canción desconocida"
    else:
      title1=data["items"][0]['snippet']['title']
      print("\tTítulo (m): ",title1)
      title_def=unidecode(title1)
      print("\tTítulo (ucde): ",title_def)
      title_f = title_def.translate({ord(c): None for c in '́´:"/\!@#$[]'})
      title_def = title_f.replace("." or ","," ")
      print("\tTítulo (def): ",title_def)
    return title_def
  except (ValueError,IndexError,KeyError,urllib.error.HTTPError):
    print("\n\t<<<<<< Error al buscar el título del vídeo | ID: ",chat_id,">>>>>>\n")
    bot.sendMessage(chat_id,"Se ha producido un error al obtener la información del vídeo que nos has mandado.\n\nRevisa que los términos introductidos están correctamente escritos o prueba con otros términos de búsqueda o no utilices caracteres especiales ([á,...,ú],ñ, ...)")

archivo_api = open("API_KEY.txt","r")
API=archivo_api.readline()