import string
import random
import hashlib


escolhas_possiveis = string.ascii_letters + string.digits

def rendom_key():
    """Gera uma string aleatoria com letras e numeros"""
    key: str = ''
    for i in range(26):
        key += random.choice(escolhas_possiveis)
    return key


def hex_crypt(password):
    """Converete a senha em hexadecimal"""
    # cria um objeto SHA-256
    sha256 = hashlib.sha256()

    # Converta a senha em bytes
    sha256.update(password.encode())

    # obtem o resultado em bytes
    senha_hash_bytes = sha256.digest()

    # converte o hash em hexadecimal
    senha_hex = senha_hash_bytes.hex()
    
    return senha_hex


def chack_password(input_password, hashed_password):
    """verifica se `input_password`  coresponde a o valor hexadecimal `hashed_password`"""
    
    # Tranforma a senha bruta em hexadecimal
    input_password = hex_crypt(input_password)

    # Verifica se a senha convertida é igual a que foi passada
    if input_password == hashed_password:
        return True
    else:
        return False 


