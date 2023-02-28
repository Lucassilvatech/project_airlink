import string
import random

escolhas_possiveis = string.ascii_letters + string.digits

def rendom_key():
    for i in range(26):
        key += random.choice(escolhas_possiveis)
    return key