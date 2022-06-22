import argparse
from dbconfig import dbconfig
from getpass import getpass
import hashlib
from rich import print as printc
from add import *


parser = argparse.ArgumentParser(description='Password Manager 1.1 --- Credit: An Duc Thien Vu')

parser.add_argument('option', help='(a)dd / (e)xtract / (g)enerate')
parser.add_argument("-s", "--name", help="Site name")
parser.add_argument("-u", "--url", help="Site URL")
parser.add_argument("-e", "--email", help="Email")
parser.add_argument("-l", "--login", help="Username")
parser.add_argument("--length", help="Length of the password to generate",type=int)
parser.add_argument("-c", "--copy", action='store_true', help='Copy password to clipboard')


args = parser.parse_args()

def user_auth():
	#Authenticate the user
	db = dbconfig()
	cursor = db.cursor()
	query = "SELECT * FROM pm.secrets"
	cursor.execute(query)
	results = cursor.fetchall()

	n = 0
	w = False
	while True:		
		mp = getpass("Enter Mater_Password: ")
		hashed_mp = hashlib.sha256(mp.encode()).hexdigest()
		if hashed_mp == results[0][0]:
			break
		n+=1
		printc(f"[red]Incorrect! You have {4-n} attempts left[/red]")
		if n == 4:
			printc("[yellow]Exiting...[/yellow]")
			w =  True
			break
		
			
	if w:
		return False
	else:
		printc("[green]Welcome![/green]")
		return [mp,results[0][1]]

def main():
	if args.option in ["add","a"]:
		if args.name == None or args.url == None or args.login == None:
			if args.name == None:
				printc("[red][!][/red] Site Name (-s) required ")
			if args.url == None:
				printc("[red][!][/red] Site URL (-u) required ")
			if args.login == None:
				printc("[red][!][/red] Site Login (-l) required ")

			return

		if args.email == None:
			args.email = ""

		auth = user_auth()

		#auth[0] = plain text mp entered by the user
		#auth[0] is used in PBKDF2 in addEntry() to create Enc. key that encrypt site password
		#auth[1] = SALT (ds)
		if auth:
			addEntry(auth[0],auth[1],args.name,args.url,args.email,args.login)


main()
			