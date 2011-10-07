import ConfigParser
import os.path

from gluon.storage import Storage
from gluon.tools import Mail, Auth

from config import ConfigFile

db = local_import('logic.db').DB()
gl = local_import('logic.globaleaks').Globaleaks(db)

mail = Mail(db)
auth = Auth(db)

cfgfile = os.path.join(os.path.dirname(__file__), 'gleaks.cfg')

# bind everything to settings
settings = Storage()
settings.globals = ConfigFile(cfgfile, 'global')
settings.private = Storage()
settings.tulip = ConfigFile(cfgfile, 'tulip')
settings.logging = ConfigFile(cfgfile, 'logging')
settings.auth = auth.settings
settings.mail = mail.settings

# GLOBAL setting
settings.private.author_email = 'info@globaleaks.org'
settings.private.database_uri = 'sqlite://storage.sqlite'
settings.private.security_key = '7a716c8b015b5caca119e195533717fe9a3095d67b3f97114e30256b27392977'
settings.private.email_server = 'localhost'
settings.private.email_sender = 'node@globaleaks.org'
settings.private.email_login = ''
settings.private.login_method = 'local'
settings.private.login_config = ''
settings.private.plugins = []
# AWS configuration
settings.private.aws_key = '<AWS-KEY>'
settings.private.aws_secret_key = '<AWS-SECRET-KEY>'
settings.private.hostname = '127.0.0.1'
settings.private.port     = '8000'

settings.mail.server = 'smtp.gmail.com:587'                    # your SMTP server
settings.mail.sender = 'globaleaks2011@gmail.com'              # your email
settings.mail.login = ''                                       # your credentials or None

# settings.auth
settings.auth.hmac_key = 'sha512:7a716c8b015b5caca119e195533717fe9a3095d67b3f97114e30256b27392977'    # before define_tables()
auth.define_tables()                                           # creates all needed tables
settings.auth.mailer = mail                                    # for user email verification
settings.auth.registration_requires_verification = False
settings.auth.registration_requires_approval = False
auth.messages.verify_email = 'Click on the link http://' + request.env.http_host + URL('default','user',args=['verify_email']) + '/%(key)s to verify your email'

settings.auth.reset_password_requires_verification = True
auth.messages.reset_password = 'Click on the link http://' + request.env.http_host + URL('default','user',args=['reset_password']) + '/%(key)s to reset your password'

settings.auth.table_user.email.label=T("Username")

