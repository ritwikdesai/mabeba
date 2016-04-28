import hashlib
import bcrypt
from M2Crypto import RSA, BIO, EVP
from M2Crypto.EVP import Cipher
from base64 import b64encode,b64decode
import pyotp
import time
from datetime import datetime
from uuid import uuid4
import hashlib
import hmac
from passlib.utils.pbkdf2 import pbkdf2

IV = '\0' * 16

KEY_128 = 16
KEY_256 = 32

ITER_1K = 1000
ITER_10K = 10000
ITER_100K = 100000
ITER_1M = 1000000

def now():
    return time.mktime(datetime.now().timetuple())



def gen_otp_secret():
    return str(pyotp.random_base32())

def totp_now(secret,interval=30):
    totp = pyotp.TOTP(secret,interval=interval)
    return totp.now()

def totp_verify(secret,code,interval=30):
    totp = pyotp.TOTP(secret,interval=interval)
    return totp.verify(code)

def secure_pw(plain_text,salt,fast = True):
    if fast is True:
        secure_pass = hashlib.md5(plain_text+salt).hexdigest()
    else:
        secure_pass = bcrypt.hashpw(plain_text,salt)

    return secure_pass


def aes_encrypt(mess,aes_key,size=256):
    if size == 128:
        algo = 'aes_128_cbc'
    elif size == 256:
        algo = 'aes_256_cbc'
    else:
        algo = 'aes_128_cbc'

    cipher = Cipher(alg=algo,key=aes_key,iv=IV,op=1)
    o = cipher.update(mess)
    o = o + cipher.final()
    del cipher

    return b64encode(o)


def gen_salt():
    return str(bcrypt.gensalt())

def key_from_pass(passwd,salt,iter,keylen):
    return b64encode(pbkdf2(passwd,salt,iter,keylen))
    return
def key_to_bytes(b64encoded):
    return b64decode(b64encoded)

def aes_decrypt(mess,aes_key,size=256):
    if size == 128:
        algo = 'aes_128_cbc'
    elif size == 256:
        algo = 'aes_256_cbc'
    else:
        algo = 'aes_128_cbc'
    mess = b64decode(mess)
    cipher = Cipher(alg=algo,key=aes_key,iv=IV,op=0)
    o = cipher.update(mess)
    o = o + cipher.final()
    del cipher

    return o

def encrypt(mess,pub_key):
    """
    Encrypt the message mess by public key pub_key
    """
    mem = BIO.MemoryBuffer(pub_key)
    key = RSA.load_pub_key_bio(mem)
    cipher = key.public_encrypt(mess,RSA.pkcs1_oaep_padding)

    return cipher.encode('base64')

def decrypt(mess,pvt_key):
    """
    Decrypts the message mess by the private key pvt_key
    """
    cipher = mess.decode('base64')
    mem = BIO.MemoryBuffer(pvt_key)
    key = RSA.load_key_bio(mem)
    try:
        plain = key.private_decrypt(cipher,RSA.pkcs1_oaep_padding)
    except:
        plain = ""

    if plain == "":
        return ""

    return plain

def gen_key_pair(bits = 2048):
    """
    Generates rsa key-pair
    """
    new_key = RSA.gen_key(bits, 65537)
    memory = BIO.MemoryBuffer()
    new_key.save_key_bio(memory, cipher=None)
    private_key = memory.getvalue()
    new_key.save_pub_key_bio(memory)
    return private_key, memory.getvalue()


# def get_random_id():
#     return str(get_random_string(length,allowed_chars='abcdefghijklmnopqrstuvwxyz1234567890'))

def get_random_id():
    return str(uuid4())


if __name__ == '__main__':
    pvt,pub = gen_key_pair(2048)

    message = raw_input('Input Message:')
    encrypted = encrypt(message,pub)
    print 'Ciphertext: ', encrypted
    print '------------------------'
    print 'Plaintext: ', decrypt(encrypted,pvt)

def get_public_key():
    f = open('/Users/ritwikdesai/Developer/PythonEnv/lib/python2.7/site-packages/sslserver/certs/development.pub')
    key = f.read()
    f.close()
    return key

def get_private_key():
    f = open('/Users/ritwikdesai/Developer/PythonEnv/lib/python2.7/site-packages/sslserver/certs/development.key')
    key = f.read()
    f.close()
    return key

def sign_msg(key,msg):
    return hmac.new(key,msg,hashlib.sha256)

