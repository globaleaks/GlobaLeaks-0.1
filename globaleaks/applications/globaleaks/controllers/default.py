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
                        tulip = "admin"
                if not tulip:
                    tulip = "admin"
                for c in form.elements('input'):
                    print c['_name']
                    if c['_name'] == "username":
                        print c
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

    # XXX
    # not so easy switch in use
    # requires=[IS_NOT_EMPTY(), IS_IN_SET([0, 1, 2, 3, 4, 5, 6, 7, 8, 9 , 0, ' '])
    # inside a form_receipt = SQLFORM.factory(Field('Receipt', requires))
    if request.vars:
        req = request.vars
        leak_number = req.Receipt.replace(' ', '')
        tulip_url = hashlib.sha256(leak_number).hexdigest()
        redirect("/globaleaks/tulip/status/" + tulip_url)

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
