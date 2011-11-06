import gluon.contrib.simplejson as json
from gluon.fileutils import copystream

import os
import shutil

def index():
    return {}

def post():
    # shutil.copyfileobj(request.body, open("/dev/null", "wb"))
    print request.env.content_length
    copystream(request.body, open('/dev/null', "wb"), int(request.env.content_length))
    return json.dumps({})
