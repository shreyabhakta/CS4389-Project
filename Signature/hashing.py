# This file signs with the owner's private key and verifes the signature using owner's public key

import rsa

# open a document and return the data inside it
def openFile(file):
    document = open(file, 'rb')
    data = document.read()
    document.close()
    return data

privateKey = rsa.PrivateKey.load_pkcs1(openFile('privateKey.key'))
dataMessage = openFile('messageData')
keyHashValue = rsa.compute_hash(dataMessage, 'SHA-512')  

# sign the given dataMessage with the owner's private key
sign = rsa.sign(dataMessage, privateKey, 'SHA-512')

signedFile = open('ownerSignature','wb')
signedFile.write(sign)

print("Signature: ", sign)

