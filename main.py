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


def encrypt_file(key, file_path):
    f = open(file_path, "r", encoding="utf-8")
    tocript = bytes(f.read(), encoding="utf-8")
    f.close()
    cripted_file = encrypt(key, tocript)
    return (cripted_file)


def decrypt_file(key, file_path):
    f = open(file_path, "rb")
    ciphertext = bytes(f.read())
    f.close()
    decripted_file = decrypt(key, ciphertext)
    return (decripted_file)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    f = open("key.txt", "r", encoding="utf-8")
    key = bytes(f.read(), encoding="utf-8")
    f.close()

    encf = encrypt_file(key,"tocript.txt")
    f = open("cripted2.txt", "wb")
    f.write(encf)


    res = decrypt(key, encf)
    print(res)

    x = decrypt_file(key, "cripted.txt")
    print(x)
    # from PIL import Image
    #
    # # Read image
    # img = Image.open('x.jpg')
    #
    # # Output Images
    # img.show()
    #
    # # prints format of image
    # print(img.format)
    #
    # # prints mode of image
    # print(img.mode)
    #
    # import sys
    from PIL import Image
    from io import BytesIO

    # PNG data
    LEFT_THUMB = (
        b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A\x00\x00\x00\x0D\x49\x48\x44\x52\x00\x00'
        b'\x00\x13\x00\x00\x00\x0B\x08\x06\x00\x00\x00\x9D\xD5\xB6\x3A\x00\x00\x01'
        b'\x2E\x49\x44\x41\x54\x78\x9C\x95\xD2\x31\x6B\xC2\x40\x00\x05\xE0\x77\x10'
        b'\x42\x09\x34\xD0\x29\x21\x82\xC9\x9C\x2E\x72\x4B\x87\x40\x50\xB9\xBF\x5B'
        b'\x28\x35\xA1\xA4\x94\x76\x68\x1C\x1C\x74\xCD\x9A\xE8\x20\x0A\x12\xA5\x5A'
        b'\xE4\x72\xC9\x75\x10\x6D\xDC\xCE\xF7\x03\x3E\xDE\x83\x47\xA4\x94\x68\x67'
        b'\xB5\xD9\x4E\xBF\xBF\x3E\xE8\x78\x3C\x86\x6A\x3C\xCF\x43\x10\x04\x20\x6D'
        b'\x6C\xB5\xD9\x4E\x93\xF8\x95\x5A\x96\x05\xC6\x98\x32\x56\x14\x05\x46\xA3'
        b'\x11\xB4\x36\x14\xBD\x3C\xD3\x4E\xA7\x03\xC6\x18\x8E\xC7\x23\x9A\xA6\x51'
        b'\xC2\x5C\xD7\x45\x9E\xE7\x27\xEC\x0C\x39\x8E\x03\xC6\x18\x0E\x87\x83\x32'
        b'\x04\x00\xE7\x75\x1A\xE7\x7C\xF2\xF9\xFE\x46\x6D\xDB\x06\x63\x0C\xFB\xFD'
        b'\x1E\x75\x5D\x2B\x43\x57\x58\xF9\xF3\xAB\xAD\xD7\x6B\x98\xA6\x09\x21\x04'
        b'\x76\xBB\x1D\x84\x10\x37\x61\x86\x61\x9C\x30\x00\x70\x1C\x07\x49\x92\x80'
        b'\x10\x82\x7E\xBF\x8F\xE5\x72\x79\x13\x78\x69\xF6\x70\x6F\x88\x5E\xAF\x37'
        b'\x2B\xCB\x92\xC6\x71\x0C\x42\x08\xC2\x30\xC4\x7C\x3E\x57\x06\x2F\x98\xAE'
        b'\xEB\x4F\xAE\xEB\x4E\x06\x83\xC1\x4C\x4A\x49\xA3\x28\x82\x94\x12\x61\x18'
        b'\x2A\x37\x5B\x2C\x16\xE8\x76\xBB\xFF\x3F\xE3\x9C\x4F\x8A\xA2\xD0\xD2\x34'
        b'\xA5\x59\x96\xA1\xAA\x2A\x65\xCC\xB2\x2C\x0C\x87\xC3\xEB\xD3\x9E\xC1\xAA'
        b'\xAA\xEE\x38\xE7\x4A\x90\xAE\xEB\x00\x00\xDF\xF7\x1F\xFF\x00\x09\x7C\xA7'
        b'\x93\xB1\xFB\xFA\x11\x00\x00\x00\x00\x49\x45\x4E\x44\xAE\x42\x60\x82'
    )

    stream = BytesIO(LEFT_THUMB)

    image = Image.open(stream).convert("RGBA")
    stream.close()
    image.show()