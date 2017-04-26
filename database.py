#!/usr/bin/python3

import pymysql 		# pip install PyMySQL

# This function reads user-database in order to get language preferences and operating system ones

def write_database(name,chat_id,lang,data):
	# Open database connection
	db = pymysql.connect("YOUR_HOST (localhost,127.0.0.1, ...)","YOUR_USER","YOUR_PASSWORD","DATABASE_TABLE_NAME",charset='utf8')

	# prepare a cursor object using cursor() method
	c = db.cursor()
	0
	#db.set_character_set('utf8')
	c.execute('SET NAMES utf8;')
	c.execute('SET CHARACTER SET utf8;')
	c.execute('SET character_set_connection=utf8;')
	# execute SQL query using execute() method.
	#cursor.execute("SELECT VERSION()")
	c.execute("""SELECT chat_id FROM Usuario WHERE chat_id = %s""", (chat_id))
	aux = c.fetchone()
	if aux == None:
		data = None
	elif aux != None:
		data = "Something"
	if data == None:
		c.execute("INSERT INTO Usuario (name, chat_id, lang) VALUES (%s, %s, %s)", (name, chat_id, lang))
		db.commit()
	else:
		c.execute("""UPDATE Usuario SET lang = %s,name = %s WHERE chat_id = %s""", (lang, name, chat_id))
		db.commit()
	# Fetch a single row using fetchone() method.
	#data = cursor.fetchone()

	#print ("Database version : %s " % data)

	# disconnect from server
	db.close()
	return 1

def read_database(chat_id):
	db = pymysql.connect("YOUR_HOST (localhost,127.0.0.1, ...)","YOUR_USER","YOUR_PASSWORD","DATABASE_TABLE_NAME",charset='utf8')
	c = db.cursor()
	0
	#db.set_character_set('utf8')
	c.execute('SET NAMES utf8;')
	c.execute('SET CHARACTER SET utf8;')
	c.execute('SET character_set_connection=utf8;')
	c.execute("""SELECT lang FROM Usuario WHERE chat_id = %s""", (chat_id))
	aux = c.fetchone()
	value = aux[0]
	db.close()
	return value

def cont_database(chat_id):
	# Open database connection
	db = pymysql.connect("YOUR_HOST (localhost,127.0.0.1, ...)","YOUR_USER","YOUR_PASSWORD","DATABASE_TABLE_NAME",charset='utf8')

	# prepare a cursor object using cursor() method
	c = db.cursor()
	0
	#db.set_character_set('utf8')
	c.execute('SET NAMES utf8;')
	c.execute('SET CHARACTER SET utf8;')
	c.execute('SET character_set_connection=utf8;')
	# execute SQL query using execute() method.
	#cursor.execute("SELECT VERSION()")
	c.execute("""SELECT cont_down FROM Usuario WHERE chat_id = %s """, (chat_id))
	aux = c.fetchone()
	if aux[0]==None:
		aux1=0
		print("\n\tNúmero de descargas actualmente: ",aux1)
	else:
		#print(aux[0])
		aux1=int(aux[0])
		print("\n\tNúmero de descargas actualmente: ",aux1)
	cont = aux1+1
	#print(cont)
	c.execute("""UPDATE Usuario SET cont_down = %s WHERE chat_id = %s""", (cont, chat_id))
	db.commit()
	# Fetch a single row using fetchone() method.
	#data = cursor.fetchone()

	#print ("Database version : %s " % data)

	# disconnect from server
	db.close()

def read_os(chat_id,name):
	db = pymysql.connect("YOUR_HOST (localhost,127.0.0.1, ...)","YOUR_USER","YOUR_PASSWORD","DATABASE_TABLE_NAME",charset='utf8')
	c = db.cursor()
	0
	#db.set_character_set('utf8')
	c.execute('SET NAMES utf8;')
	c.execute('SET CHARACTER SET utf8;')
	c.execute('SET character_set_connection=utf8;')
	c.execute("""SELECT OS FROM Usuario WHERE chat_id = %s""", (chat_id))
	aux = c.fetchone()
	aux1=aux[0]
	#print(aux1)
	db.close()
	return aux1

def write_os(chat_id,name,os):
	db = pymysql.connect("YOUR_HOST (localhost,127.0.0.1, ...)","YOUR_USER","YOUR_PASSWORD","DATABASE_TABLE_NAME",charset='utf8')
	c = db.cursor()
	0
	#db.set_character_set('utf8')
	c.execute('SET NAMES utf8;')
	c.execute('SET CHARACTER SET utf8;')
	c.execute('SET character_set_connection=utf8;')
	c.execute("""UPDATE Usuario SET OS = %s WHERE chat_id = %s""", (os, chat_id))
	db.commit()
	db.close()

def read_audio(chat_id):
	db = pymysql.connect("YOUR_HOST (localhost,127.0.0.1, ...)","YOUR_USER","YOUR_PASSWORD","DATABASE_TABLE_NAME",charset='utf8')
	c = db.cursor()
	0
	c.execute('SET NAMES utf8;')
	c.execute('SET CHARACTER SET utf8;')
	c.execute('SET character_set_connection=utf8;')
	c.execute("""SELECT audio_quality FROM Usuario WHERE chat_id = %s""",(chat_id))
	aux = c.fetchone()
	value = aux[0]
	db.close()
	return value

def set_audio(chat_id,value):
	db = pymysql.connect("YOUR_HOST (localhost,127.0.0.1, ...)","YOUR_USER","YOUR_PASSWORD","DATABASE_TABLE_NAME",charset='utf8')
	c = db.cursor()
	0
	c.execute('SET NAMES utf8;')
	c.execute('SET CHARACTER SET utf8;')
	c.execute('SET character_set_connection=utf8;')
	c.execute("""UPDATE Usuario SET audio_quality = %s WHERE chat_id = %s""",(value,chat_id))
	db.commit()
	db.close()