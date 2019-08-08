import os
import struct

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto.Cipher import AES
from Crypto import Random

def genKeyPair(keysize):
  random_generator = Random.new().read
  new_key = RSA.generate(keysize, random_generator)
  private_key = new_key.exportKey("PEM")
  public_key = new_key.publickey().exportKey("PEM")
  return public_key, private_key

def genAESKey():
  secret = os.urandom(16)
  return secret, AES.new(secret)

def importPublicKey(filename):
  fd = open(filename, "rb")
  public_key_file = fd.read()
  fd.close()
  public_key = RSA.importKey(public_key_file)
  return public_key

def importPrivateKey(filename):
  fd = open(filename, "rb")
  private_key_file = fd.read()
  fd.close()
  private_key = RSA.importKey(private_key_file)
  return private_key

def rsaEncrypt(binary, public_key):
  cipher = PKCS1_OAEP.new(public_key)
  return cipher.encrypt(binary)

def rsaDecrypt(binary, private_key):
  cipher = PKCS1_OAEP.new(private_key)
  return cipher.decrypt(binary)

def aesEncryptFile(infilename, outfilename, public_key):
  chunksize = 16
  infile = open(infilename, "rb")
  outfile = open(outfilename, "wb")
  filesize = os.path.getsize(infilename)
  secret, cipher = genAESKey()
  encrypted_secret = rsaEncrypt(secret, public_key)
  iv = Random.new().read(16)
  encryptor = AES.new(secret, AES.MODE_CBC, iv)
  outfile.write(struct.pack('<Q', filesize))
  outfile.write(encrypted_secret)
  outfile.write(iv)

  while True:
    chunk = infile.read(chunksize)
    if len(chunk) == 0:
      break
    elif len(chunk) % 16 != 0:
      chunk += b' ' * (16 - len(chunk) % 16)
    outfile.write(encryptor.encrypt(chunk))
  infile.close()
  outfile.close()


def aesDecryptFile(infilename, outfilename, private_key):
  chunksize = 16
  infile = open(infilename, "rb")
  outfile = open(outfilename, "wb")
  filesize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
  encrypted_secret = infile.read(128)
  secret = rsaDecrypt(encrypted_secret, private_key)
  iv = infile.read(16)
  decryptor = AES.new(secret, AES.MODE_CBC, iv)
  while True:
    chunk = infile.read(chunksize)
    if len(chunk) == 0:
      break
    outfile.write(decryptor.decrypt(chunk))
  outfile.truncate(filesize)


