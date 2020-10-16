# This file will generate and write public and private keys to the respective filenames

import rsa

# generate public and private keys 
(publicKey, privateKey) = rsa.newkeys(2048)

with open('publicKey.key', 'wb') as files:
    files.write(publicKey.save_pkcs1('PEM'))

with open('privateKey.key', 'wb') as files:
    files.write(privateKey.save_pkcs1('PEM'))
