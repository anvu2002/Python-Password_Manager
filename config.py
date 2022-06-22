from dbconfig import dbconfig
from getpass import getpass
from rich import print as printc
from rich.console import Console
import hashlib
import string
import random

console = Console()

def SALT_generate(length=10):
	return ''.join(random.choices(string.ascii_uppercase + string.digits, k = length))
	


def config():
	#Create a Database
	db = dbconfig() #get [db object]
	cursor = db.cursor() #to run query

	printc("[blue][+]Checking current configuration-------")
	query = "SHOW DATABASES LIKE 'pm'"
	res = cursor.execute(query)
	if res == 1:
		print("Found pm database")
		uI = input("Do you want to reset it?(Y/N)")
		if uI == 'Y' or uI =='y':			
			printc("[green][+][/green]Dropped pm database!")		
			cursor.execute("drop database pm;")
		else:
			printc("[green][+] ------Displaying current data------- [/green]")
			#cursor.execute("")


	printc("[green][+] ------Creating new config------- [/green]")

	try:
		cursor.execute("CREATE DATABASE pm")
	except Exception as e:
		printc("[red][!] An error occured while trying to creat db 'pm'.")
		console.print_exeception(show_locals=True)
		sys.exit(0)
	printc("[green][+][/green] Database 'pm' created")

	#Creat Tables:
	query = "CREATE TABLE pm.secrets (masterpass_hash TEXT not null, device_secret TEXT not null)"
	res = cursor.execute(query)
	printc("[green][+][/green] Tabe 'secrets' created")
  	
	query = 'CREATE TABLE pm.fields (sitename TEXT not null, siteurl TEXT not null, email TEXT, username TEXT, password TEXT not null)'
	res = cursor.execute(query)
	printc("[green][+][/green] Tabe 'fields' created")

  	#Ask for MasterPassword
	while True:
		mp = getpass("Enter a MASTER PASSWORD: ")
		if mp == getpass("Re-type: ") and mp!="":
			break #Valid input -->Exit out the loop!
		printc("[yellow][-] Please enter again.[/yellow]")
  	
  	#Hash the MasterPassword --- SHA256 
	hashed_mp = hashlib.sha256(mp.encode()).hexdigest()
	printc("[green][+][/green] Generated hash of MASTER PASSWORD")
	
	#Generate SALT for PBKDF2:	d
	salt = SALT_generate()
	printc("[green][+][/green]Salt generated")

	#Insert salt, and MasterPassword_hash into table:
	query= "INSERT INTO pm.secrets (masterpass_hash,device_secret) values (%s, %s)"
	val = (hashed_mp, salt)
	cursor.execute(query, val)
	db.commit()

	printc("[green][+][/green] Added salt, mp_hashed to secrets table")
	printc("[green][+][/green]---------Finished Master Password Configuration---------")
	db.close()

config()