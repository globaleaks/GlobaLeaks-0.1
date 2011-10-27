from gluon.storage import Storage
from gluon.tools import Mail, Auth
from gluon.tools import Recaptcha

gl = local_import('logic.globaleaks').Globaleaks(db)

mail = Mail(db)
auth = Auth(db)

# bind everything to settings
settings.private = Storage()
settings.tulip = ConfigFile(cfgfile, 'tulip')
settings.logging = ConfigFile(cfgfile, 'logging')
settings.auth = auth.settings
settings.mail = mail.settings

# XXX: hack
settings.mail.__dict__['commit'] = db.commit
settings.auth.__dict__['commit'] = db.commit

#
# reCAPTCHA support
auth.settings.captcha = Recaptcha(request,
        '6LdZ9sgSAAAAAAg621OrrkKkrCjbr3Zu4LFCZlY1',
        '6LdZ9sgSAAAAAAJCZqqo2qLYa2wPzaZorEmc-qdJ')

# Set up the logger to be shared with all
logger = local_import('logger').start_logger(settings.logging)

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

