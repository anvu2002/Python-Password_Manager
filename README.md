# Python-Password_Manager
## Motivation
Portfolio building - Site passwords management using python modules to encrypt password and manage data through MariaDB

## Features
This CLI program allows users to manage passwords and other information corresponding to a site. They only need to provide a single Master Password that will give access to all stored information, with the site passwords are hidden and encrypted with AES 256.<br>
The information is saved in MariaDB database.<br>
The sites’ passwords are {hidden} when the entries are displayed in the CLI, and they could be copied to a clipboard through specified options.<br>
The sites’ passwords can be auto-generated randomly to further the secure for its users. 

### Requirements
```
pip install backports.pbkdf2
service mysql start
pip install rich
```

## Usages
```
Usage:

Password Manager 1.1 --- Credit: An Duc Thien Vu

positional arguments:
  option                (a)dd / (e)xtract / (g)enerate

optional arguments:
  -h, --help            show this help message and exit
  -s NAME, --name NAME  Site name
  -u URL, --url URL     Site URL
  -e EMAIL, --email EMAIL
                        Email
  -l LOGIN, --login LOGIN
                        Username
  --length LENGTH       Length of the password to generate
  -c, --copy            Copy password to clipboard
                                                       

```
Example:
```
python config
python3 -m Password_Manager add -s facebook -u facebook.com -l user123

```
## Background
[+] MASTER PASSWORD: the initial text input enterer by the users, hashed and saved in pm.secretes<br>
[+] SALT – Secrete Value: an IV value used in HMAC method to protect Master Password Hash, saved in a pm.secretes<br>
[+] MASTER KEY: encryption key AES<br>
AES-256 will be used to provide encryption for specified fields. Since the cipher requires a specific encryption key        length such as 256 bits long, yet the inputs by the users could be vary. In this case, PBKDF2 is used as a key stretching  technique<br>
		PBKDF2 = HMAC-SHA256 (Master Password + SALT) --> hashing function = valid key for AES-256<br>
Encrypted fields: email, username, sites’ passwords<br>
Plain fields: sitename, URLs<br>
[+] Process:
MasterPassword is inputted as plaintext then hashed by the program. It compares that hashed value against the stored hash in the database; if matches, the user is authenticated. MasterKey is then created = PBKDF2 (MasterPassword_PlainText + SALT). The user starts inputting for fields such as site names, URLs, username, email, and password; with the last 3 fields are encrypted with MaterKey<br>.
With 
```
-c: decrypt and copy site's password to clipboard
```
MasterPassword is asked, then validates by hashing that user-inputted value and compare against the stored hash<br>
MasterKey is then created (PBKDF of MasterPassword + SALT)<br>
Decrypt Site’s passwords with MasterKey and copy to clipboard<br>



