import ConfigParser
import os.path

from gluon.storage import Storage
from config import ConfigFile, cfgfile

class ThreadSafe(dict):
    forever=10**10
    def __init__(self):
         import thread
         self['lock']=thread.allocate_lock()
    def __setattr__(self,key,value):
         self['lock'].acquire()
         self[key]=value
         self['lock'].release()
    def __getattr__(self,key):
         self['lock'].acquire()
         value=self[key]
         self['lock'].release()
         return value

#x=cache.ram('elefante_in_sala_server',lambda:ThreadSafe(),ThreadSafe.forever)


################################################################
# Import the database and global settings from the config file #
################################################################
settings = Storage()
settings.globals = ConfigFile(cfgfile, 'global')
settings.database = ConfigFile(cfgfile, 'database')

response.headers.pop('X-Powered-By')
response.headers['Server'] = settings.globals.servername

default_lang = settings.globals.language
T.set_current_languages(default_lang, default_lang)
plugin_translate_current_language = default_lang
session._language = request.vars._language or session._language or plugin_translate_current_language
T.force(str(session._language))

