import gluon.contrib.simplejson as json
import os

def index():
    return {}

def post():
    with open(os.devnull, "w") as null:
        null.write("".join(request.body.readlines()))
    return json.dumps({})
