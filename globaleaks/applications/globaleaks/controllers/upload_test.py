import gluon.contrib.simplejson as json
from gluon.fileutils import copystream

import os
import shutil

def index():
    return {}

def post():
    try:
        a = request.body.read()
        return json.dumps({"A": "B"})
    except:
        return json.dumps({"C": "D"})
