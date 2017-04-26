from urllib.request import urlopen
import urllib.error
import ujson as json
from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

def getVidId(query,chat_id,bot,update):
  try:
    print("\n-----------------------------------------------------------------------------------------------------------------")
    print ("Debug [2]")
    print("-----------------------------------------------------------------------------------------------------------------")
    query1=query.split()
    query2=('+').join(query1)
    url="https://www.googleapis.com/youtube/v3/search?part=id%2Csnippet&maxResults=1&q={}&key={}".format(query2,API)
    print ("\tEnlace de la API (1): ",url)

    response=urlopen(url)
    json_text=response.read()
    data=json.loads(json_text)
    vidId=data["items"][0]['id']['videoId']
    return vidId
  except (ValueError,IndexError,KeyError,urllib.error.HTTPError):
    print("\n\t<<<<<< Error al buscar la ID del vídeo | ID: ",chat_id,">>>>>>>\n")
    bot.sendMessage(chat_id,"No hemos encontrado ninguna canción en base a los términos de búsqueda introducidos.\n\nPrueba a escribir sin tildes o busca tu vídeo con @vid directamente desde el teclado (escribe /help para obtener más ayuda).")

archivo_api = open("API_KEY.txt","r")
API=archivo_api.readline()