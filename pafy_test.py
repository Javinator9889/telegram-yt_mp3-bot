import pafy 					# pip install pafy (for downloading YouTube videos)
from pydub import AudioSegment 	# pip install pydub ('libavtools' and 'ffmpeg' requiered. Check "https://github.com/jiaaro/pydub#installation" for getting assistance)
import os
import os.path as path
import threading
from database import read_database,write_database,cont_database,read_os,read_audio
from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import telegram
import time
from gmusicapi import Mobileclient  # pip install gmusicapi ('libavtools' and 'ffmpeg' requiered. Check "http://unofficial-google-music-api.readthedocs.io/en/latest/usage.html#usage" for getting assistance)
import gmusicapi 					# Get metadata from Google Play Music
import urllib.request
import youtube_dl
from curl import descarga

def key_f(bot, update,chat_id):
    keyboard = [[InlineKeyboardButton("Sí, hay fallos", callback_data='1'),InlineKeyboardButton("No 👌", callback_data='2')]]
    reply_markup2 = InlineKeyboardMarkup(keyboard)
    bot.sendMessage(chat_id,text="¿Ha habido algún error en la canción descargada?\n\n_(Responder es opcional. Únicamente es para ofrecerte la mejor ayuda posible)_",
      parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup2)

def key_fen(bot,update,chat_id):
    keyboard = [[InlineKeyboardButton("Yes, help me", callback_data='1'),InlineKeyboardButton("No 👌", callback_data='2')]]
    reply_markup2 = InlineKeyboardMarkup(keyboard)
    bot.sendMessage(chat_id,text="Is there any problem with the downloaded file?\n\n_(Answering is optional. It's only for giving you the best help possible)_",
      parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup2)

def key_iosen(bot,update,chat_id):
    keyboard = [[InlineKeyboardButton("Yes", callback_data='5'),InlineKeyboardButton("No", callback_data='6')]]
    reply_markup2 = InlineKeyboardMarkup(keyboard)
    bot.sendMessage(chat_id,text="Are you an *iOS user* _(iPhone / iPad)_?",
      parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup2)

def key_ios(bot,update,chat_id):
    keyboard = [[InlineKeyboardButton("Sí", callback_data='3'),InlineKeyboardButton("No", callback_data='4')]]
    reply_markup2 = InlineKeyboardMarkup(keyboard)
    bot.sendMessage(chat_id,text="¿Tu dispositivo *tiene iOS* _(iPhone / iPad)_?",
      parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=reply_markup2)

def ask_for_credentials():
    """Make an instance of the api and attempts to login with it.
    Return the authenticated api.
    """

    # We're not going to upload anything, so the Mobileclient is what we want.
    api = Mobileclient()

    logged_in = False
    attempts = 0

    while not logged_in and attempts < 100:
        email = "YOUR_GMAIL"
        password = "YOUR_PASSWORD"

        logged_in = api.login(email, password, Mobileclient.FROM_MAC_ADDRESS)
        attempts += 1

    return api

def video_down(bot,update,chat_id,user):
	try:
		title_file="title_{}.txt".format(chat_id)
		video_file = "url_{}.txt".format(chat_id)
		link = open(video_file,'r')
		titulo = open(title_file,'r')
		url = link.readline()
		name = titulo.readline()
		print("\n\tEnlace de YouTube: ",url)
		print("\n\tTítulo: ",name)
		full_name="{}_{}.".format(name,chat_id)
		link.close()
		titulo.close()
		titulo_2 = name.translate({ord(c): None for c in '()[]-'})
		titulo_3 = titulo_2.replace("feat","")
		titulo_4 = titulo_3.replace("Lyrics" or "lyrics" or "LYRICS","")
		titulo_5 = titulo_4.replace("Audio Only" or "audio Only" or "audio only","")
		titulo_6 = titulo_5.replace("Official video" or "Official Video" or "Official" or "official" or "OFFICIAL","")
		titulo_7 = titulo_6.replace("LIVE" or "Live" or "live","")
		titulo_8 = titulo_7.replace("Cover" or "COVER" or "cover","")
		titulo_9 = titulo_8.replace("short" or "Short" or "SHORT","")
		titulo_10 = titulo_9.replace("HD","")
		titulo_11 = titulo_10.replace("Version" or "version" or "VERSION","")
		titulo_12 = titulo_11.replace("Video" or "video" or "VIDEO","")
		titulo_13 = titulo_12.replace("long" or "Long" or "LONG","")
		titulo_14 = titulo_13.replace("Lyric" or "lyric" or "LYRIC","")
		titulo_15 = titulo_14.replace("  "," ")
		print("\n\tTítulo de búsqueda: ",titulo_14)
		idioma = read_database(chat_id)
		cont_database(chat_id)
		ad_quality = read_audio(chat_id)
		if ad_quality == None:
			ad_quality = "256k"
		if ad_quality == "120k":
			calidad = "baja"
			calidad_en = "low"
		elif ad_quality == "256k":
			calidad = "media"
			calidad_en = "medium"
		elif ad_quality == "320k":
			calidad = "alta"
			calidad_en = "high"
		time.sleep(2)
		cov_name = "cover_{}.jpg".format(chat_id)
		if 'es' in idioma:
			bot.sendMessage(chat_id,text="Estamos descargando la canción en *calidad "+calidad+"* (cámbialo en /preferences).\n\nComo este bot está pensado para descargar música, buscaremos el *título, artista, etc* _independientemente de lo que hayas enviado_\n\n\nPor favor, espere...\n\n*NOTA: si observa que la velocidad de descarga es muy lenta, acceda a* /errors *para obtener asistencia e información*",
				parse_mode=telegram.ParseMode.MARKDOWN)
		elif 'en' in idioma:
			bot.sendMessage(chat_id,text="We are downloading the song in *"+calidad_en+" quality* (change it in /preferences).\n\nAs this is a bot for downloading music, we will search for *title, artist, etc* _regardless of what you've sent_\n\n\nPlease wait ...\n\n*INFO: If you notice that the download speed is very slow, access* /errors *for assistance and information*",
				parse_mode=telegram.ParseMode.MARKDOWN)
		api = ask_for_credentials()
		song = api.search(titulo_14,max_results=1)
		try:
			album = song['song_hits'][0]['track']['album']
			print("\n\tAlbum encontrado")
		except IndexError:
			print("Error al conseguir el álbum")
			album = "Unknown"
		try:
			artist = song['song_hits'][0]['track']['albumArtist']
			print("\tArtista encontrado")
		except IndexError:
			print("Error al conseguir el nombre del artista")
			artist = "Unknown"
		try:
			cover_url = song['song_hits'][0]['track']['albumArtRef'][0]['url']
			urllib.request.urlretrieve(cover_url, cov_name)
			picture = cov_name
			print("\tCarátula encontrada")
		except IndexError:
			print("Error al conseguir la carátula del álbum")
			picture = "default.png"
		try:
			titulo_met = song['song_hits'][0]['track']['title']
			print("\tTítulo encontrado")
		except IndexError:
			print("Error al conseguir el título de la canción")
			titulo_met = name
		video = pafy.new(url)
		audio = video.getbestaudio()  # 'webm' has always the best quality audio (on YouTube)
		print("\n\tEntrado dentro de la sección de descarga...","//",threading.currentThread().getName(),"//")
		print("\n\tFormato de audio: ",audio.extension)
		audio.download(quiet=False,filepath=full_name+audio.extension)  # 'quiet=False' shows a progress bar
		full_name_w="{}_{}.{}".format(name,chat_id,audio.extension)
		full_name_m="{}_{}.mp3".format(name,chat_id)
		if (os.path.getsize(full_name_w)>=25000000): # For converting this huge files it's needed a bit more time than others
			if 'es' in read_database(chat_id):
				bot.sendMessage(chat_id,"Ya tenemos tu canción lista 🙂\nComo es un poco más grande de lo normal, tardará un poquito más en enviarse _(pero no hay de qué preocuparse 😉)_",
					parse_mode=telegram.ParseMode.MARKDOWN)
			elif 'en' in read_database(chat_id):
				bot.sendMessage(chat_id,"We have your song ready 🙂\nAs it is a bit bigger than the others, it will take us a bit longer to send it to you _(but you don't have to worry about anything 😉)_",
					parse_mode=telegram.ParseMode.MARKDOWN)
		print("\n\tConvirtiendo a mp3...")
		AudioSegment.from_file(full_name_w,audio.extension).export(full_name_m,format="mp3",bitrate=ad_quality,cover=picture,tags={'artist': artist, 'album': album, 'title': titulo_met})
		if path.exists(full_name_w):
			os.remove(full_name_w)
		if path.exists(cov_name):
			os.remove(cov_name)
		song = open(full_name_m,"rb")
		print("\n\tEnviando canción...")
		if (os.path.getsize(full_name_m)>=50000000): 	# Telegram limits bot sendable-file to 50MB
			raise telegram.error.TelegramError('El archivo en formato MP3 es mayor de 50 MB - Se envía directamente')
		else:
			bot.sendAudio(chat_id,song)
			print ("Completado","//",threading.currentThread().getName(),"//")
			song.close()
			if 'es' in read_database(chat_id):
				bot.sendMessage(chat_id,"La descarga de tu canción ha finalizado",
					parse_mode=telegram.ParseMode.MARKDOWN)
				if read_os(chat_id,user) == None:
					key_ios(bot,update,chat_id)
				elif 'iOS' in read_os(chat_id,user): 	# If device is iOS, we provide a direct download link (because iOS devices cannot obtain downloaded data between apps)
					bot.sendMessage(chat_id,text="Has establecido tu dispositivo como un *iOS*, por lo que procedemos a enviarle un enlace de descarga directa (para cambiar este valor, ejecute /preferences).\n\n_Por favor, espere_",
						parse_mode=telegram.ParseMode.MARKDOWN)
					url_file = descarga(chat_id,name)
					bot.sendMessage(chat_id,text="Aquí tienes tu [enlace de descarga directa]("+url_file+").",parse_mode=telegram.ParseMode.MARKDOWN)
					try:
						if path.exists(title_file):
							os.remove(title_file)
						if path.exists(video_file):
							os.remove(video_file)
						if path.exists(full_name_m):
							os.remove(full_name_m)
						key_f(bot,update,chat_id)
					except PermissionError:
						key_f(bot,update,chat_id)
				else:
					try:
						if path.exists(title_file):
							os.remove(title_file)
						if path.exists(video_file):
							os.remove(video_file)
						if path.exists(full_name_m):
							os.remove(full_name_m)
						key_f(bot,update,chat_id)
					except PermissionError:
						key_f(bot,update,chat_id)
			elif 'en' in read_database(chat_id):
				bot.sendMessage(chat_id,"We have just finished downloading your song",
					parse_mode=telegram.ParseMode.MARKDOWN)
				if read_os(chat_id,user) == None:
					key_iosen(bot,update,chat_id)
				elif 'iOS' in read_os(chat_id,user):
					bot.sendMessage(chat_id,text="You have setted your device as an *iOS*, so we are preparing a direct download link for you (for changing this value, use /preferences).\n\n_Please, wait_",
						parse_mode=telegram.ParseMode.MARKDOWN)
					url_file = descarga(chat_id,name)
					bot.sendMessage(chat_id,text="Here you have [your direct download link]("+url_file+").",parse_mode=telegram.ParseMode.MARKDOWN)
					try:
						if path.exists(title_file):
							os.remove(title_file)
						if path.exists(video_file):
							os.remove(video_file)
						if path.exists(full_name_m):
							os.remove(full_name_m)
						key_fen(bot,update,chat_id)
					except PermissionError:
						key_fen(bot,update,chat_id)
				else:
					try:
						if path.exists(title_file):
							os.remove(title_file)
						if path.exists(video_file):
							os.remove(video_file)
						if path.exists(full_name_m):
							os.remove(full_name_m)
						key_fen(bot,update,chat_id)
					except PermissionError:
						key_fen(bot,update,chat_id)
			print("Canción enviada correctamente")
	except telegram.error.TelegramError:
		print("\n\"TelegramError\" - Mostrando mensaje...","//",threading.currentThread().getName(),"//")
		if 'es' in read_database(chat_id):
			bot.sendMessage(chat_id,text="*¡¡Ups!!* 😱\n\nDebido a que tu archivo es bastante grande _(>50 MB)_, no te lo *podemos enviar directamente por Telegram*, por lo que lo estamos subiendo a un servidor para que lo puedas *descargar directamente*.\n\nMantente a la espera y en nada tendrás tu descarga lista 👌",
				parse_mode=telegram.ParseMode.MARKDOWN)
		elif 'en' in read_database(chat_id):
			bot.sendMessage(chat_id,text="*¡¡Wooha!!* 😱\n\nYour file is too big _(>50 MB)_, so we *can't send it by Telegram*, but don't worry because we're uploading it to a server in order to *let you download it directly*.\n\nWait for a time and you'll have your download ready 👌",
				parse_mode=telegram.ParseMode.MARKDOWN)
		url_file = descarga(chat_id,name)
		time.sleep(1)
		if 'es' in read_database(chat_id):
			bot.sendMessage(chat_id,text="Aquí tienes tu [enlace de descarga directa]("+url_file+"). Tienes *una semana entera* para utilizar el enlace anterior, luego se eliminará.",
				parse_mode=telegram.ParseMode.MARKDOWN)
		elif 'en' in read_database(chat_id):
			bot.sendMessage(chat_id,text="Here you have [your direct download link]("+url_file+"). You have *a hole week* to use that link, then it will be deleted from server.",
				parse_mode=telegram.ParseMode.MARKDOWN)
		try:
			if path.exists(title_file):
				os.remove(title_file)
			if path.exists(video_file):
				os.remove(video_file)
			if path.exists(full_name_m):
				song.close()
				os.remove(full_name_m)
		except PermissionError:
			print("\n\tError en los permisos (el archivo/s están siendo utilizados)")
			print("Limpiando búffer y cerrando","//",threading.currentThread().getName(),"//")
			sys.stdout.flush()
			sys.stdin.flush()
			print("//",threading.currentThread().getName(),"//","cerrado correctamente")
	except (OSError,youtube_dl.utils.ExtractorError,youtube_dl.utils.DownloadError) as e:
		try:
			full_name_w="{}_{}.{}".format(name,chat_id,audio.extension)
			full_name_m="{}_{}.mp3".format(name,chat_id)
			if 'es' in read_database(chat_id):
				bot.sendMessage(chat_id,text="No hemos podido descargar tu vídeo por temas de *Copyright*. _Sentimos mucho las molestias_",parse_mode=telegram.ParseMode.MARKDOWN)
				try:
					if path.exists(title_file):
						os.remove(title_file)
					if path.exists(video_file):
						os.remove(video_file)
					if path.exists(full_name_m):
						song.close()
						os.remove(full_name_m)
					if path.exists(full_name_w):
						os.remove(full_name_w)
				except PermissionError:
					print("\n\tError en los permisos (el archivo/s están siendo utilizados)")
					print("Limpiando búffer y cerrando","//",threading.currentThread().getName(),"//")
					sys.stdout.flush()
					sys.stdin.flush()
					print("//",threading.currentThread().getName(),"//","cerrado correctamente")
			elif 'en' in read_database(chat_id):
				bot.sendMessage(chat_id,text="We couldn't download your video because of *Copyright conditions*. _We're sorry for the inconvenience_",parse_mode=telegram.ParseMode.MARKDOWN)
				try:
					if path.exists(title_file):
						os.remove(title_file)
					if path.exists(video_file):
						os.remove(video_file)
					if path.exists(full_name_m):
						song.close()
						os.remove(full_name_m)
					if path.exists(full_name_w):
						os.remove(full_name_w)
				except PermissionError:
					print("\n\tError en los permisos (el archivo/s están siendo utilizados)")
					print("Limpiando búffer y cerrando","//",threading.currentThread().getName(),"//")
					sys.stdout.flush()
					sys.stdin.flush()
					print("//",threading.currentThread().getName(),"//","cerrado correctamente")
		except UnboundLocalError:
			if 'es' in read_database(chat_id):
				bot.sendMessage(chat_id,text="No hemos podido descargar tu vídeo por temas de *Copyright*. _Sentimos mucho las molestias_",parse_mode=telegram.ParseMode.MARKDOWN)
				try:
					if path.exists(title_file):
						os.remove(title_file)
					if path.exists(video_file):
						os.remove(video_file)
				except PermissionError:
					print("\n\tError en los permisos (el archivo/s están siendo utilizados)")
					print("Limpiando búffer y cerrando","//",threading.currentThread().getName(),"//")
					sys.stdout.flush()
					sys.stdin.flush()
					print("//",threading.currentThread().getName(),"//","cerrado correctamente")
			elif 'en' in read_database(chat_id):
				bot.sendMessage(chat_id,text="We couldn't download your video because of *Copyright conditions*. _We're sorry for the inconvenience_",parse_mode=telegram.ParseMode.MARKDOWN)
				try:
					if path.exists(title_file):
						os.remove(title_file)
					if path.exists(video_file):
						os.remove(video_file)
				except PermissionError:
					print("\n\tError en los permisos (el archivo/s están siendo utilizados)")
					print("Limpiando búffer y cerrando","//",threading.currentThread().getName(),"//")
					sys.stdout.flush()
					sys.stdin.flush()
					print("//",threading.currentThread().getName(),"//","cerrado correctamente")
