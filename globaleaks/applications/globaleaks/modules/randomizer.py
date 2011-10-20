import random
import hashlib, os
import string

def generate_tulip_receipt():
    #FIXME is this a good idea?
    #      should i be converting the random number string to bytes?
    number = ""
    for i in range(0,10):
        number += str(ord(os.urandom(1)) % 10)
    return (number, hashlib.sha256(number).hexdigest())

def generate_wb_id():
    #FIXME is this a good idea?
    #      should i be converting the random number string to bytes?
    return hashlib.sha256(os.urandom(1024)).hexdigest()

def generate_dirname():
    return hashlib.sha256(os.urandom(1024)).hexdigest()

def generate_leaker_id():
    return hashlib.sha256(os.urandom(1024)).hexdigest()

def generate_tulip_url():
    return hashlib.sha256(os.urandom(100)).hexdigest()

def generate_target_passphrase():
    number = ""
    for i in range(0,14):
        number += str(ord(os.urandom(1)) % 10)
    return (number, hashlib.sha256(number).hexdigest())

def alphanumeric(n):
    output = ""
    for i in range(1, n):
        output += random.choice(string.ascii_letters+string.digits)
    return output
