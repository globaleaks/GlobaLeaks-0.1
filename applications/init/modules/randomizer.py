import random
import hashlib, os

def generate_leaker_id():
    return hashlib.sha256(os.urandom(100)).hexdigest()
    
def generate_tulip_url():
    return hashlib.sha256(os.urandom(100)).hexdigest()

