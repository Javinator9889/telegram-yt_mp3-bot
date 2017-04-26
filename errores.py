import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# This file has multiple keyboards for '/errors' interaction. It uses basically ReplyKeyboardMarkup for substitute Telegram keyboard with different options

def mensaje_bot(bot,update,chat_id):
	bot.sendMessage(chat_id,text="*Contesta al siguiente formulario para ofrecerte la mejor ayuda posible y así solucionar los errores*",
		parse_mode=telegram.ParseMode.MARKDOWN)
	key_b(bot,update,chat_id)

def message_bot(bot,update,chat_id):
    bot.sendMessage(chat_id,text="*Please, answer this form in order to offer you the best help possible and solve the errors*",
        parse_mode=telegram.ParseMode.MARKDOWN)
    key_ben(bot,update,chat_id)

def key_ben(bot, update,chat_id):
    keyboard = [
    ['While downloading','Other...']
    ]
    reply_markup = ReplyKeyboardMarkup(
    keyboard = keyboard, 
    resize_keyboard=True, 
    one_time_keyboard=True)
    bot.sendMessage(chat_id=chat_id,
        text="_When are you having your error?_ *(use the keyboard that appears just below)*",
        parse_mode=telegram.ParseMode.MARKDOWN, 
        reply_markup=reply_markup)

def key_eden(bot,update,chat_id):
    keyboard = [
    ['Empty file (0.00 Bytes)','Video can\'t be downloaded'],
    ['The bot is not responding','Downloading very slowly'],
    ['Another error not registered']
    ]
    reply_markup = ReplyKeyboardMarkup(
    keyboard = keyboard, 
    resize_keyboard=True, 
    one_time_keyboard=True)
    bot.sendMessage(chat_id=chat_id,
        text="_Choose what has happened to you below the following options:_",
        parse_mode=telegram.ParseMode.MARKDOWN, 
        reply_markup=reply_markup)

def key_oen(bot,update,chat_id):
    keyboard = [
    ['Error while searching the song','The bot is not responding'],
    ['Show all registered errors','Another error not registered']
    ]
    reply_markup = ReplyKeyboardMarkup(
    keyboard = keyboard, 
    resize_keyboard=True, 
    one_time_keyboard=True)
    bot.sendMessage(chat_id=chat_id,
        text="_Choose what has happened to you below the following options:_",
        parse_mode=telegram.ParseMode.MARKDOWN, 
        reply_markup=reply_markup)

def key_b(bot, update,chat_id):
    keyboard = [
    ['Al descargar','Otro...']
    ]
    reply_markup = ReplyKeyboardMarkup(
    keyboard = keyboard, 
    resize_keyboard=True, 
    one_time_keyboard=True)
    bot.sendMessage(chat_id=chat_id,
        text="_¿Qué tipo de error has tenido?_ *(utiliza el teclado que aparece justo debajo)*",
        parse_mode=telegram.ParseMode.MARKDOWN, 
        reply_markup=reply_markup)

def key_ed(bot,update,chat_id):
    keyboard = [
    ['Archivo vacío (0.00 Bytes)','El vídeo no puede ser obtenido'],
    ['El bot no hace nada','Descarga muy lenta'],
    ['Otro error no registrado']
    ]
    reply_markup = ReplyKeyboardMarkup(
    keyboard = keyboard, 
    resize_keyboard=True, 
    one_time_keyboard=True)
    bot.sendMessage(chat_id=chat_id,
        text="_De las opciones posibles, indica cuál te ha ocurrido a ti:_",
        parse_mode=telegram.ParseMode.MARKDOWN, 
        reply_markup=reply_markup)

def key_o(bot,update,chat_id):
    keyboard = [
    ['Error al buscar la canción','El bot no hace nada'],
    ['Mostrar todos los errores','Otro error no registrado']
    ]
    reply_markup = ReplyKeyboardMarkup(
    keyboard = keyboard, 
    resize_keyboard=True, 
    one_time_keyboard=True)
    bot.sendMessage(chat_id=chat_id,
        text="_De las opciones posibles, indica cuál te ha ocurrido a ti:_",
        parse_mode=telegram.ParseMode.MARKDOWN, 
        reply_markup=reply_markup)