from random import randint


def generate_code():
    return hex(randint(0x0, 0xFFFFFF)).split('x')[1].upper()
