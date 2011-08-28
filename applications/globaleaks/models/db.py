# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

import time

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
#########################################################################

"""
if request.env.web2py_runtime_gae:            # if running on Google App Engine
    db = DAL('google:datastore')              # connect to Google BigTable
                                              # optional DAL('gae://namespace')
    session.connect(request, response, db = db) # and store sessions and tickets there
    ### or use the following lines to store sessions in Memcache
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
else:                                         # else use a normal relational database
    db = DAL('sqlite://storage.sqlite')       # if not, use SQLite or other DB
"""
randomizer = local_import('randomizer')

class DB(DAL):
    def __init__(self):
        DAL.__init__(self, 'sqlite://storage.db')
        self.create_db()
    
    def create_db(self):
        self.define_table('target',
            Field('name'),
            Field('category'),
            Field('desc'),
            Field('uri'),
            Field('type'),
            Field('info'),
            Field('status'),
            Field('last_sent_tulip'),
            Field('last_access'),
            Field('last_download'),
            Field('tulip_counter'),
            Field('dowload_counter'),
            format='%(name)s'
           )
            
        self.define_table('leak',
            Field('title'),
            Field('desc'),
            Field('submission_timestamp'),
            Field('leaker_id', self.target),
            format='%(name)s'
            )
            
        self.define_table('comment',
            Field('leak_id', self.leak),
            Field('commenter_id', self.target),
            Field('comment'),
            format='%(name)s'
            )
    
        self.define_table('material',
            Field('url', unique=True),
            Field('leak_id', self.leak),
            Field('type'),
            format='%(name)s'
            )
            
        self.define_table('tulip',
            Field('uri', unique=True),
            Field('leak_id', self.leak),
            Field('target_id'),# self.target),
            Field('downloads_counter'),
            Field('allowed_downloads'),
            Field('expiry_time'),
            format='%(name)s'
            )

db = DB()

####
# The main GlobaLeaks Class
###

class Globaleaks(object):

    def __init__(self):
        pass
        
    def create_target(self, name, category, desc, uri, type, info):
        target_id = db.target.insert(name=name, 
            category=category,
            desc = desc, uri=uri, type=type, info=info,
            status=True #, last_send_tulip=None,
            #last_access=None, last_download=None,
            #tulip_counter=None, download_counter=None
           )
        db.commit()
        return target_id
        
    def delete_target (self, id):
       db(db.target.id==id).delete()
       pass

    def get_targets(self):
        return db(db.target).select()
        
        
    def get_target(self, target_id):
        pass
        
    def create_leak(self, title, desc, leaker, material, targets = {}, tags=""):
        #FIXME insert new tags into DB first
        
        #Create leak and insert into DB
        leak_id = db.leak.insert(title = title, desc = desc,
            submission_timestamp = time.time(),
            leaker_id = 0)
        
        #Create a tulip for each target and insert into DB
        for target_uri, allowed_downloads in targets.iteritems():
            db.tulip.insert(uri = randomizer.generate_tulip_url(),
                leak_id = leak_id,
                target_id = target_uri, #FIXME get target_id_properly
                downloads_counter = 0,
                allowed_downloads = allowed_downloads,
                expiry_time = 0)
        
        db.commit()
        return leak_id
        
    def get_leaks(self):
        pass
        
    def get_leak(self, leak_id):
        pass
        
    def get_tulips(self, leak_id):
        pass
        
    def get_tulip(self, tulip_id):
        pass




####
# For the time being just use sqlite
###

# db = DAL('sqlite://storage.sqlite')

# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'


# Waste of time and useless piece of shit
# response.generic_patterns = ['*'] if request.is_local else []

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Mail, Auth, Crud, Service, PluginManager, prettydate
mail = Mail()                                  # mailer
auth = Auth(db)                                # authentication/authorization
crud = Crud(db)                                # for CRUD helpers using auth
service = Service()                            # for json, xml, jsonrpc, xmlrpc, amfrpc
plugins = PluginManager()                      # for configuring plugins

# mail.settings.server = 'logging' or 'smtp.gmail.com:587'  # your SMTP server
# mail.settings.sender = 'you@gmail.com'         # your email
# mail.settings.login = 'username:password'      # your credentials or None

auth.settings.hmac_key = 'sha512:7a716c8b015b5caca119e195533717fe9a3095d67b3f97114e30256b27392977'   # before define_tables()
auth.define_tables()                           # creates all needed tables
auth.settings.mailer = mail                    # for user email verification
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+URL('default','user',args=['verify_email'])+'/%(key)s to verify your email'

auth.settings.reset_password_requires_verification = True
auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL('default','user',args=['reset_password'])+'/%(key)s to reset your password'



#########################################################################
## If you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, uncomment and customize following
# from gluon.contrib.login_methods.rpx_account import RPXAccount
# auth.settings.actions_disabled = \
#    ['register','change_password','request_reset_password']
# auth.settings.login_form = RPXAccount(request, api_key='...',domain='...',
#    url = "http://localhost:8000/%s/default/user/login" % request.application)
## other login methods are in gluon/contrib/login_methods
#########################################################################


# XXX
# Don't know
# crud.settings.auth = None        # =auth to enforce authorization on crud

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

# mail.settings.server = settings.email_server
# mail.settings.sender = settings.email_sender
# mail.settings.login = settings.email_login

gl = Globaleaks()
