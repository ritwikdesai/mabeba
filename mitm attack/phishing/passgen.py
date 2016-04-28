import os, random, string


def passgen(len = 8):
    if len < 8:
        len = 8
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    random.seed = (os.urandom(1024))

    return ''.join(random.choice(chars) for i in range(len))