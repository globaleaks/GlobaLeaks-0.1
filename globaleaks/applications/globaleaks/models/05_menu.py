response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%s <%s>' % (settings.author, settings.author_email)
response.meta.keywords = settings.keywords
response.meta.description = settings.description

response.menu = [
    (T('Index'),URL('default','index')==URL(),URL('default','index'),[]),
    (T('Submission'),URL('submission', 'index')==URL(),URL('submission','index'),[]),
]

response.menu_target = [
    (T('Tulip'),'/globaleaks/tulip/status/'+str(session.target)==URL(), '/globaleaks/tulip/status/'+str(session.target)),
    (T('Bouquet'),'/globaleaks/target/bouquet/'+str(session.target)==URL(), '/globaleaks/target/bouquet/'+str(session.target)),
]

response.menu_admin = [
    (T('Receivers'),'/globaleaks/admin/targets'==URL(), '/globaleaks/admin/targets'),
    (T('Stats'),'/globaleaks/admin/statistics'==URL(), '/globaleaks/admin/statistics/'),
    (T('Logout'),'/globaleaks/default/user/logout'==URL(), '/globaleaks/default/user/logout'),
    (T('Password'),'/globaleaks/default/user/change_password'==URL(), '/globaleaks/default/user/change_password'),
]
