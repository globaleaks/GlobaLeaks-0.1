#coding: utf-8
"""
Controller for the index
"""
from __future__ import with_statement
import logging

session.admin = False
session.taget = False

### required - do not delete
def user():
    """
    Controller for user login
    """
    tulip = None
    form = auth()
    try:
        if (request.vars['_next']):
            print "contains next..."
            next = request.vars['_next']
            if type(next) is str:
                path = next.split("/")
            else:
                path = next[0].split("/")
            print next
            if len(path) > 2:
                print "path > 3"
                if len(path) > 0 and path[2] == "tulip":
                    print path[4]
                    try:
                        tulip = Tulip(url=path[4]).target
                    except:
                        tulip = "admin"
                if not tulip:
                    tulip = "admin"
                for c in form.elements('input'):
                    print c['_name']
                    if c['_name'] == "username":
                        print c
                        c['_value'] = tulip
                return dict(form=form)
    except:
        print "except"
    
    try:
        for c in form.elements('input'):
            print c['_name']
            if c['_name'] == "username":
                print c
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


def index():
    """
    Controller for GlobaLeaks index page
    """
    import hashlib

    tulip_url = None

    if request.vars:
        req = request.vars
        # Make the tulip work well
        leak_number = req.Receipt.replace(' ', '')
        tulip_url = hashlib.sha256(leak_number).hexdigest()
        redirect("/tulip/" + tulip_url)

    with open(settings.globals.presentation_file) as filestream:
        presentation_text = filestream.read()
        # sadly, HTML must not be passed, to avoid XXSs

    return dict(tulip_url=None, presentation_text=presentation_text)

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
