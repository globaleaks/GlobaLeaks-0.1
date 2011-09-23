from ConfigParser import ConfigParser
import os.path

from gluon.storage import Storage
from gluon.tools import Mail, Auth

db = local_import('logic.db').DB()
gl = local_import('logic.globaleaks').Globaleaks(db)

mail = Mail(db)
auth = Auth(db)
settings = Storage()

cfgparser = ConfigParser()
cfgfile = os.path.join(os.path.dirname(__file__), 'gleaks.cfg')
cfgparser.read([cfgfile])

# GLOBAL setting
settings.migrate = True
settings.title = cfgparser.get('global', 'title')
settings.subtitle = cfgparser.get('global', 'subtitle')
settings.author = cfgparser.get('global', 'author')
settings.author_email = 'info@globaleaks.org'
settings.keywords = cfgparser.get('global', 'html_keyword')
settings.description = cfgparser.get('global', 'description')
settings.layout_theme = cfgparser.get('global', 'layout_theme')
settings.database_uri = 'sqlite://storage.sqlite'
settings.security_key = '7a716c8b015b5caca119e195533717fe9a3095d67b3f97114e30256b27392977'
settings.email_server = 'localhost'
settings.email_sender = 'node@globaleaks.org'
settings.email_login = ''
settings.login_method = 'local'
settings.login_config = ''
settings.plugins = []

settings.hostname = '127.0.0.1'
settings.port     = '8000'

# TULIP settings
settings.tulip.max_access = cfgparser.get('tulip', 'max_access', 10)
settings.tulip.expire = cfgparser.get('tulip', 'expire', 6)

# MAIL settings
mail.settings.server = 'smtp.gmail.com:587'                    # your SMTP server
mail.settings.sender = 'globaleaks2011@gmail.com'              # your email
mail.settings.login = ''                                       # your credentials or None

# AUTH settings
auth.settings.hmac_key = 'sha512:7a716c8b015b5caca119e195533717fe9a3095d67b3f97114e30256b27392977'    # before define_tables()
auth.define_tables()                                           # creates all needed tables
auth.settings.mailer = mail                                    # for user email verification
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.messages.verify_email = 'Click on the link http://' + request.env.http_host + URL('default','user',args=['verify_email']) + '/%(key)s to verify your email'

auth.settings.reset_password_requires_verification = True
auth.messages.reset_password = 'Click on the link http://' + request.env.http_host + URL('default','user',args=['reset_password']) + '/%(key)s to reset your password'

auth.settings.table_user.email.label=T("Username")

# AWS configuration
settings.aws_key = '<AWS-KEY>'
settings.aws_secret_key = '<AWS-SECRET-KEY>'


