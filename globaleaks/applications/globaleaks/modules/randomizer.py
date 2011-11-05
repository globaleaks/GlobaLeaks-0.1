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

def __sanitize_title(title):
    import unicodedata
    title = unicode(title, "utf-8")
    title = "".join([c for c in title if unicodedata.category(c)[0] == "L"])
    return title

# Maybe these three should be merged into one
def generate_human_dirname(request, leak, old_dirname):
    # Name like Data-$Title-$ID-$progressivo-.zip
    prog = 1
    title = __sanitize_title(leak.title)
    dirname = "Data-%s-%s-%s" % (title, old_dirname[:4], str(prog))
    while os.path.exists(os.path.join(request.folder, 'material', dirname)):
        prog += 1
        dirname = "Data-%s-%s-%s" % (title, old_dirname[:4], str(prog))
    return dirname

def is_human_dirname(dirname):
    return dirname.startswith("Data-")

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

#
def alphanumeric(n):
    output = ""
    for i in range(1, n):
        output += random.choice(string.ascii_letters+string.digits)
    return output
