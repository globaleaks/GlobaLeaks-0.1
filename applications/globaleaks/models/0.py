from gluon.storage import Storage
settings = Storage()

settings.migrate = True
settings.title = 'GlobaLeaks'
settings.subtitle = 'Open Source Whistleblowing Platform'
settings.author = 'RGC'
settings.author_email = 'info@globaleaks.org'
settings.keywords = ''
settings.description = ''
settings.layout_theme = 'Default'
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


