#coding: utf-8
"""
Controller for the index
"""
from __future__ import with_statement
import logging
import os

session.admin = False
session.taget = False

def user():
    """
    Controller for user login
    """
    tulip = None
    form = auth()
    if '_next' in request.vars:
        next = request.vars['_next']
        # XXX: what the hell is this shit?
        if not isinstance(next, str):
            next = next[0]
        else:
            path = next.split(os.sep)
            if len(path) > 2:
                # print "path > 3"
                if len(path) > 0 and path[2] == "tulip":
                    # print path[4]
                    try:
                        tulip = Tulip(url=path[4]).target
                    except:
                        pass
                if not tulip:
                    tulip = "admin"
                for c in form.elements('input'):
                    if c['_name'] == "username":
                        c['_value'] = tulip
                return dict(form=form)
    try:
        for c in form.elements('input'):
            if c['_name'] == "username":
                c['_value'] = "admin"
    except:
        pass
    return dict(form=form)


def download():
    return response.download(request, db)


def call():
    session.forget()
    return service()
### end requires

@configuration_required
def index():
    """
    Controller for GlobaLeaks index page
    """
    import hashlib

    tulip_url = None

    if request.vars:
        req = request.vars
        leak_number = req.Receipt.replace(' ', '')
        tulip_url = hashlib.sha256(leak_number).hexdigest()
        redurl = "/globaleaks/tulip/status/" + tulip_url
        redirect(redurl)

    with open(settings.globals.presentation_file) as filestream:
        presentation_html = filestream.read()

    return dict(tulip_url=None, presentation_html=presentation_html)

def notfound():
    logging.debug('404 Error detected')
    return dict()

def oops():
    logging.error('Error %s : %%(ticket)s.' % request.url)
    return dict()

def error():
    return {}

def email_template():
    return {}
