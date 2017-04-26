import threading
from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from pafy_test import video_down

# This function distributes song-download requests for each user, creating a thread (process) for allowing multi-download

def sender(bot,update,chat_id,name):
  proc_name = "{}+{}".format(chat_id,name)
  thread = threading.Thread(target=video_down,name=proc_name,args=(bot,update,chat_id,name,))
  thread.start()


archivo_api = open("API_KEY.txt","r")
API=archivo_api.readline()