import os
from Crypto.Cipher import AES

key = os.urandom(16)
nonce = os.urandom(8)

# encrypt
cipher_enc = AES.new(key, AES.MODE_CTR, nonce=nonce)    # Noncompliant {{(BlockCipher) AES-CTR}}
pt = b"a secret message"
ct = cipher_enc.encrypt(pt)

# decrypt
cipher_dec = AES.new(key, AES.MODE_CTR, nonce=nonce)    # Noncompliant {{(BlockCipher) AES-CTR}}
res = cipher_dec.decrypt(ct)






