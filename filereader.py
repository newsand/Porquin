from PIL import Image
from io import BytesIO
from Crypto import Random
from Crypto.Cipher import Blowfish
from struct import pack

def encrypt(key, file):
    bs = Blowfish.block_size
    iv = Random.new().read(bs)
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    plaintext = file
    plen = bs - divmod(len(plaintext), bs)[1]
    padding = [plen] * plen
    padding = pack('b' * plen, *padding)
    text = cipher.IV + cipher.encrypt(plaintext + padding)
    return (text)


def decrypt(key, file):
    bs = Blowfish.block_size

    ciphertext = file
    iv = ciphertext[:bs]
    ciphertext = ciphertext[bs:]

    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    msg = cipher.decrypt(ciphertext)

    last_byte = msg[-1]
    msg = msg[:- (last_byte if type(last_byte) is int else ord(last_byte))]

    return msg.decode('utf-8')
def decryptimg(key, file):
    bs = Blowfish.block_size

    ciphertext = file
    iv = ciphertext[:bs]
    ciphertext = ciphertext[bs:]

    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    msg = cipher.decrypt(ciphertext)

    last_byte = msg[-1]
    msg = msg[:- (last_byte if type(last_byte) is int else ord(last_byte))]

    return msg
def decrypt_file(key, file_path):
    f = open(file_path, "rb")
    ciphertext = bytes(f.read())
    f.close()
    decripted_file = decrypt(key, ciphertext)
    return (decripted_file)

def decrypt_img_file(key, file_path):
    f = open(file_path, "rb")
    ciphertext = bytes(f.read())
    f.close()
    decripted_file = decryptimg(key, ciphertext)
    return (decripted_file)

if __name__ == '__main__':
    f = open('x.jpg', "rb")
    ciphertext = bytes(f.read())
    f.close()
    f = open("key.txt", "r", encoding="utf-8")
    key = bytes(f.read(), encoding="utf-8")
    f.close()
    encfile = encrypt(key,ciphertext)
    f = open("y.jpg", "wb")
    f.write(encfile)
    f.close()

    new_img = decrypt_img_file(key,'y.jpg')

    #stream = BytesIO(ciphertext)
    stream = BytesIO(new_img)
    image = Image.open(stream).convert("RGBA")
    stream.close()
    image.show()