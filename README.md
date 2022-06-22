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

