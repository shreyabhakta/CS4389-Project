# This file verifies if the owner's signature is valid or not

import rsa

# open a document and return the data inside it
def openFile(file):
    document = open(file, 'rb')
    data = document.read()
    document.close()
    return data

publicKey = rsa.PublicKey.load_pkcs1(openFile('publicKey.key'))
dataMessage = openFile('messageData')
sign = openFile('ownerSignature')

# verify owner's signature 
try:
    rsa.verify(dataMessage, sign, publicKey)
    print("Congratulations!!! Owner's signature is verified.")
except:
    print("Oops!!! Owner's signature is not verified.")