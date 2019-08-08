from encrypt import *

public_key, private_key = genKeyPair(1024)
fd = open("private_key.pem", "wb")
fd.write(private_key)
fd.close()
fd = open("public_key.pem", "wb")
fd.write(public_key)
fd.close()