from getpass import getpass
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
import hashlib
from rich import print as printc

import AES_encrypt
from dbconfig import dbconfig

def addEntry(mp, ds, sitename, siteurl, email, username):
	#get the password
	site_password = getpass("Password for the site: ")


	encrypted = AES_encrypt.encrypt(source=site_password, masterPassword = mp,SALT=ds)

	#Add to db
	db = dbconfig()
	cursor = db.cursor()
	query = 'INSERT INTO pm.fields (sitename, siteurl, email, username, password) values (%s, %s, %s, %s, %s)'
	val = (sitename, siteurl, email, username, encrypted)
	cursor.execute(query, val)
	db.commit()

	printc(f"[green][+][/green] Added an entry for {sitename} site ")