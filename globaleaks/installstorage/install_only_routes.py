default_application = 'globaleaks'
default_controller  = 'default'
default_function    = 'index'

routes_in = (
             ('^/js', '/globaleaks/preload/js'),
             ('^/css', '/globaleaks/preload/css'),
             ('^/nodeprivacy(/)?', '/globaleaks/admin/nodeprivacy'),
             ('/.*tulip.*', '/globaleaks/installation/configuration.html'),
             ('/.*admin.*', '/globaleaks/installation/configuration.html'),
             ('/.*target.*', '/globaleaks/installation/configuration.html'),
             ('^/index.*', '/globaleaks/installation/configuration.html'),
             ('/', '/globaleaks/installation/configuration.html')
            )


