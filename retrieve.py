import dbconfig
from rich import print as printc
from rich.console import Console
from rich.table import Table
from getpass import getpass
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
from rich import print as printc
import pyperclip

import aesutil


def computeMasterKey(mp, ds):
	masterPassword = mp.encode()
	salt = ds.encode()
	key = PBKDF2(masterPassword, salt, 32, count=1000000, hash_mac_module=SHA512)
	return key


def retreiveEntries(mp, ds, search, decryptPassword = False):
	db = dbconfig()
	cursor = db.cursor()

	query = ""

	if len(search) == 0:
		query = "SELECT * FROM pm.fields"
	else:
		query = "SELECT * FROM pm.fields WHERE "
		#For each value in search (each search values
		for i in search: 
			query+= f"{i} = '{search[i]}' AND "
		query = query[:-5]

	cursor.execute(query)
	results = cursor.fetchall()

	if len(results) ==0:
		printc("[yellow][-][/yellow] Found nothing!")
		return

	#ecryptPassword = True --> user wants to access / copy site passwords to clipboard
	if (decryptPassword and len(results)>1) or (not decryptPassword):
		table = Table(title='Results')
		table.add_column('Site Name')
		table.add_column('URL')
		table.add_column('Email')
		table.add_column('Username')
		table.add_column('Password')

		for i in results:
			table.add_row(i[0],i[1],i[2],i[3],"{hidden}")

		console = Console()
		console.print(table)

		return

	if len(results)==1 and decryptPassword:
		mk = computeMasterKey(mp, ds)
		decrypted = aesutil.decrypt(key=mk, source = results[0][4], keyType = "bytes")

		pyperclip.copy(decrypted.decode())
		printc("[green][+][/green] Password copied to clipboard")

	db.close()