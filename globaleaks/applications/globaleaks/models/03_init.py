from gluon.storage import Storage
from gluon.tools import Mail, Auth
from gluon.tools import Crud, Service, PluginManager, prettydate

crud = Crud(db)             # for CRUD helpers using auth
service = Service()         # for json, xml, jsonrpc, xmlrpc, amfrpc
plugins = PluginManager()   # for configuring plugins

# bind everything to settings
settings.private = Storage()
settings.tulip = ConfigFile(cfgfile, 'tulip')
settings.logging = ConfigFile(cfgfile, 'logging')

# GLOBAL setting
settings.private.author_email = settings.globals.author_email
settings.private.database_uri = settings.database.uri
settings.private.security_key = settings.globals.security_key
settings.private.email_server = settings.globals.email_server
settings.private.email_sender = settings.globals.email_sender
settings.private.email_login = settings.globals.email_login
settings.private.login_method = settings.globals.login_method
settings.private.login_config = ''
settings.private.plugins = []
settings.private.hiddenservice = settings.globals.hiddenservice

# Language settings
T.set_current_languages('en', 'en-en')

if T.accepted_language != session._language:
    import re
    lang = re.compile('\w{2}').findall(session._language)[0]
    print "In here.. %s" % lang
    a = URL(r=request,c='static',f='plugin_translate/jquery.translate-1.4.3-debug-all.js')
    b = URL(r=request,c='plugin_translate',f='translate',args=lang+'.js')
    print "a: %s b: %s" % (a,b)
    response.files.append(a)
    response.files.append(b)
    print "RF: %s" % response.files

def plugin_translate(languages=[('en','English'),('es','Spanish'),('fr','French'),('de','German')]):
    return FORM(SELECT(
            _onchange="document.location='%s?_language='+jQuery(this).val()" \
                % URL(r=request,args=request.args),
            value=session._language,
            *[OPTION(k,_value=v) for v,k in languages]))


# mail and auth are filled after the first settings.tulip initialization,
# because used inside Globaleaks object
# gl = local_import('logic.globaleaks').Globaleaks(db, settings)
gl = Globaleaks()

mail = Mail(db)
auth = Auth(db)

settings.auth = auth.settings
settings.mail = mail.settings
# XXX: hack
settings.mail.__dict__['commit'] = db.commit
settings.auth.__dict__['commit'] = db.commit

# reCAPTCHA support
#from gluon.tools import Recaptcha
#auth.settings.captcha = Recaptcha(request,
#        '6LdZ9sgSAAAAAAg621OrrkKkrCjbr3Zu4LFCZlY1',
#        '6LdZ9sgSAAAAAAJCZqqo2qLYa2wPzaZorEmc-qdJ')


# Disable remember me on admin login
auth.settings.remember_me_form = False

# Disable sensitive auth actions (list from http://web2py.com/book/default/chapter/08)
auth.settings.actions_disabled.append('register') #disable register
auth.settings.actions_disabled.append('verify_email') #disable register
auth.settings.actions_disabled.append('retrieve_username') #disable register
auth.settings.actions_disabled.append('reset_password') #disable register
auth.settings.actions_disabled.append('request_reset_password') #disable register
auth.settings.actions_disabled.append('impersonate') #disable register
auth.settings.actions_disabled.append('') #disable register

auth.settings.create_user_groups = False

# Set up the logger to be shared with all
logger = local_import('logger').start_logger(settings.logging)


# AWS configuration
settings.private.aws_key = '<AWS-KEY>'
settings.private.aws_secret_key = '<AWS-SECRET-KEY>'
settings.private.hostname = '127.0.0.1'
settings.private.port     = '8000'
settings.private.mail_use_tls = True


# Mail setup
settings.mail.server = 'box218.bluehost.com:25'
settings.mail.sender = 'GlobaLeaks Demo <demonotification@globaleaks.org>'
settings.mail.login = 'demonotification@globaleaks.org:antaniglobaleaks'
settings.mail.ssl = False

mail.settings.server = settings.mail.server
mail.settings.sender = settings.mail.sender
mail.settings.login = settings.mail.login


# settings.auth
settings.auth.hmac_key = 'sha512:7a716c8b015b5caca119e195533717fe9a3095d67b3f97114e30256b27392977'    # before define_tables()

auth.define_tables(username=True)


if auth.id_group("admin"):
    settings.private.admingroup = auth.id_group("admin")
else:
    auth.add_group('admin', 'Node admins')

if auth.id_group("targets"):
    settings.private.admingroup = auth.id_group("targets")
else:
    auth.add_group('targets', 'Targets')

if auth.id_group("candelete"):
    settings.private.admingroup = auth.id_group("candelete")
else:
    auth.add_group('candelete', 'candelete')

settings.auth.mailer = mail                                    # for user email verification
settings.auth.registration_requires_verification = False
settings.auth.registration_requires_approval = False
auth.messages.verify_email = 'Click on the link http://' + request.env.http_host + \
        URL('default','user',args=['verify_email']) + '/%(key)s to verify your email'

settings.auth.reset_password_requires_verification = True
auth.messages.reset_password = 'Click on the link http://' + request.env.http_host + \
        URL('default','user',args=['reset_password']) + '/%(key)s to reset your password'

settings.auth.table_user.email.label=T("Username")

randomizer = local_import('randomizer')

tor = local_import('anonymity').Tor(settings)
