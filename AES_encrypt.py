from base64 import b64encode, b64decode
import hashlib
from Cryptodome.Cipher import AES
import os
from Cryptodome.Random import get_random_bytes



def computeMasterKey(mp, ds):
    masterPassword = mp.encode() #mp here is PLAIN_TEXT
    salt = ds.encode()
    #encryption_key  = PBKDF2(masterPassword, salt, 32, count=1000000, hmac_hash_module=SHA256) #256 bits
    encryption_key = hashlib.pbkdf2_hmac('sha256', masterPassword, salt, 1000000) #512bits long

    #print(f"MasterKey = {len(encryption_key)}")
    return encryption_key #bytes


def encrypt(source, masterPassword,ds):
    private_key = computeMasterKey(masterPassword, ds)

    # create cipher config
    cipher_config = AES.new(private_key, AES.MODE_GCM)

    # return a dictionary with the encrypted text
    encrypted_password, tag = cipher_config.encrypt_and_digest(bytes(source, 'utf-8'))

    res =  {
        'encrypted_password': b64encode(encrypted_password).decode('utf-8'),
        'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
        'tag': b64encode(tag).decode('utf-8')
        }
    #return b64encode(encrypted_password).decode('utf-8')    

    for x, y in res.items():
      if x == 'encrypted_password':
          return y
          break

def decrypt(enc_dict, password):
    # decode the dictionary entries from base64
    salt = b64decode(enc_dict['salt'])
    cipher_text = b64decode(enc_dict['cipher_text'])
    nonce = b64decode(enc_dict['nonce'])
    tag = b64decode(enc_dict['tag'])
    

    # generate the private key from the password and salt
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

    # create the cipher config
    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

    # decrypt the cipher text
    decrypted = cipher.decrypt_and_verify(cipher_text, tag)

    return decrypted
  



