default_application = 'globaleaks'
default_controller  = 'default'
default_function    = 'index'

routes_in = (
             ('^/tulip(/)?', '/globaleaks/tulip/index'),
             ('^/tulip/(?P<tulip_id>[\w]+)', '/globaleaks/tulip/status/\g<tulip_id>'),
             ('^/submit(/)?(?P<any>.*)', '/globaleaks/submission/\g<any>'),
            )

