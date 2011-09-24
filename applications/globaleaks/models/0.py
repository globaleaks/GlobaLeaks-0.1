import ConfigParser
import os.path

from gluon.storage import Storage
from gluon.tools import Mail, Auth

db = local_import('logic.db').DB()
gl = local_import('logic.globaleaks').Globaleaks(db)

mail = Mail(db)
auth = Auth(db)
#
#############################
#beginning of another file
class ConfigFile(Storage):

    def __init__(self, cfgparser, section):
        super(ConfigFile, self).__init__()

        self._cfgparser = cfgparser
        self._section = section

    def __getattr__(self, name):
        if name.startswith('_'):
            return self.__dict__.get(name, None)
        try:
            return self._cfgparser.get(self._section, name)
        except ConfigParser.NoOptionError:
            raise NameError

    def __setattr__(self, name, value):
        # keep an open port with private attributes
        if name.startswith('_'):
            self.__dict__[name] = value
        try:
            self._cfgparser.set(self._section, name, value)
        except ConfigParser.NoOptionError:
            raise NameError
#
# end of another file
##############################

cfgparser = ConfigParser.ConfigParser()
cfgfile = os.path.join(os.path.dirname(__file__), 'gleaks.cfg')
cfgparser.read(cfgfile)

# bind everything to settings
settings = Storage()
settings.globals = ConfigFile(cfgparser, 'global')
settings.tulip = ConfigFile(cfgparser, 'tulip')
settings.auth = auth.settings
settings.mail = mail.settings

# GLOBAL setting
# settings.globals.migrate = True
# settings.globals.title = procfgparser.get('global', 'title')
# settings.globals.subtitle = cfgparser.get('global', 'subtitle')
# settings.globals.author = cfgparser.get('global', 'author')
# settings.globals.author_email = 'info@globaleaks.org'
# settings.globals.keywords = cfgparser.get('global', 'html_keyword')
# settings.globals.description = cfgparser.get('global', 'description')
# settings.globals.layout_theme = cfgparser.get('global', 'layout_theme')
# settings.globals.database_uri = 'sqlite://storage.sqlite'
# settings.globals.security_key = '7a716c8b015b5caca119e195533717fe9a3095d67b3f97114e30256b27392977'
# settings.globals.email_server = 'localhost'
# settings.globals.email_sender = 'node@globaleaks.org'
# settings.globals.email_login = ''
# settings.globals.login_method = 'local'
# settings.globals.login_config = ''
# settings.globals.plugins = []
#
# settings.globals.hostname = '127.0.0.1'
# settings.globals.port     = '8000'
#
# # TULIP settings
# settings.tulip.max_access = cfgparser.get('tulip', 'max_access', 10)
# settings.tulip.expire = cfgparser.get('tulip', 'expire', 6)
#
# settings.mail
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

# AWS configuration
settings.aws_key = '<AWS-KEY>'
settings.aws_secret_key = '<AWS-SECRET-KEY>'


