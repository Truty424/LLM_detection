import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7


def encrypt_decrypt_aes_cbc_pkcs7():
    key = os.urandom(32)
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    plaintext = b"a secret message"

    # ---- Encrypt ----
    padder = PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_data) + encryptor.finalize()

    # ---- Decrypt ----
    decryptor = cipher.decryptor()
    padded_res = decryptor.update(ct) + decryptor.finalize()

    unpadder = PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_res = unpadder.update(padded_res) + unpadder.finalize()

    return unpadded_res


def camellia():
    key = os.urandom(32)
    iv = os.urandom(16)
    # Create a cipher object
    cipher = Cipher(algorithms.Camellia(key), modes.OFB(iv))  # Noncompliant {{(BlockCipher) Camellia}}

    # Encrypt
    encryptor = cipher.encryptor()
    ct = encryptor.update(b"a secret message") + encryptor.finalize()


if __name__ == "__main__":
    print(encrypt_decrypt_aes_cbc_pkcs7())
    print(camellia())
