import gluon.contrib.simplejson as json
import os
import shutil

def index():
    return {}

def post():
    shutil.copyfileobj(request.body, open("/dev/null", "wb"))
    return json.dumps({})
