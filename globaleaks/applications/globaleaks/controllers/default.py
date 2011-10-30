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
    return dict(form=auth())


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
