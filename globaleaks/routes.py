default_application = 'globaleaks'
default_controller  = 'default'
default_function    = 'index'

routes_in = (
             ('^/tulip(/)?', '/globaleaks/tulip/index'),
             ('^/targets(/)?', '/globaleaks/admin/targets'),
             ('^/tulip/(?P<tulip_id>[\w]+)', '/globaleaks/tulip/status/\g<tulip_id>'),
             ('^/submit(/)?(?P<any>.*)', '/globaleaks/submission/\g<any>'),
             ('^/subscribe(/)?', '/globaleaks/target/subscribe/'),
             ('^/unsubscribe(/)?', '/globaleaks/target/unsubscribe/'),
             ('^/groups(/)?', '/globaleaks/admin/targetgroups'),
             ('^/globalview(/)?', '/globaleaks/target/view'),
             ('^/receiver(/)?', '/globaleaks/target/receiver'),
             ('^/bouquet/(?P<target_id>[\w]+)', '/globaleaks/target/bouquet/\g<target_id>'),
             ('^/bouquet', '/globaleaks/target/bouquet')
            )


