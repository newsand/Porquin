from Crypto import Random
from Crypto.Cipher import Blowfish
from struct import pack
from io import BytesIO


class Porquicypher:

    def __init__(self, key: str):
        self.key = key.encode("utf-8")

    def encrypt(key: bytes, file: bytes):
        bs = Blowfish.block_size
        iv = Random.new().read(bs)
        cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
        plaintext = file
        plen = bs - divmod(len(plaintext), bs)[1]
        padding = [plen] * plen
        padding = pack('b' * plen, *padding)
        text = cipher.IV + cipher.encrypt(plaintext + padding)
        return text

    def decrypt(self, file):
        bs = Blowfish.block_size
        ciphertext = file
        iv = ciphertext[:bs]
        ciphertext = ciphertext[bs:]
        cipher = Blowfish.new(self.key, Blowfish.MODE_CBC, iv)
        msg = cipher.decrypt(ciphertext)
        last_byte = msg[-1]
        msg = msg[:- (last_byte if type(last_byte) is int else ord(last_byte))]

        # return msg.decode('utf-8')
        return msg

    def decrypt_image(self,file):
        #keyz = 'senhasatanica'.encode("utf-8")
        cripted_file = self.decrypt(self.key, file)
        stream = BytesIO(cripted_file).read()

        return stream