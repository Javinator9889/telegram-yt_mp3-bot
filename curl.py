import requests
import ujson as json
import unicodedata
from unidecode import unidecode
import re

def descarga(full_name):
	url = 'https://file.io/?expires=1w'
	files = {'file': open(full_name,'rb')}
	print("\n\tSubiendo archivo a 'file.io'")
	link = None
	n=0
	while link==None: 												 	 # For ensuring that the file is uploaded correctly
		response = requests.post(url, files=files)
		test = response.text
		print("JSON recibido: ",test)
		decoded = unidecode(test) 									 	 # It's needed to decode text for avoiding 'bytes' problems (b'<meta...)
		print("JSON decodificado: ",decoded)
		if '<html>' in decoded: 									 	 # When upload fails, 'file.io' sends a message with <html> header.
			print("\n\tFallo al subir el archivo. Reintentando... #",n)	 # If it's detected, assings 'link = None' and then 'while' loop restars
			link = None
			n=n+1 													 	 # Little counter
		else:
			json_data = json.loads(decoded)
			link = json_data['link']
			print("\n\nEnlace de descarga directa: ",link)
	return link