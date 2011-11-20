response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%s <%s>' % (settings.author, settings.author_email)
response.meta.keywords = settings.keywords
response.meta.description = settings.description


# Is this menu required?
response.menu = [
    (T('Index'),URL('default','index')==URL(),URL('default','index'),[]),
    (T('Submission'),URL('submission', 'index')==URL(),URL('submission','index'),[]),
#    (T('Receiver'), '/globaleaks/target/receiver'==URL(), '/globaleaks/target/receiver', []),
#    (T('Node View'), '/globaleaks/target/view'==URL(), '/globaleaks/target/view', []),
#    (T('Receivers'),'/globaleaks/admin/targets'==URL(), '/globaleaks/admin/targets'),
#    (T('Groups'),'/globaleaks/admin/targetgroups'==URL(),'/globaleaks/admin/targetgroups'),
#    (T('Tulips'),URL('tulip','index')==URL(),URL('tulip','index'),[]),
#    # "Tulips" redirect to index, why keeping that ?
]

response.menu_target = [
    (T('Tulip'),'/globaleaks/tulip/status/'+str(session.target)==URL(), '/globaleaks/tulip/status/'+str(session.target)),
#   (T('Preferences'),'/preferences'==URL(),'/preferences'),
    (T('Bouquet'),'/globaleaks/target/bouquet/'==URL(), '/globaleaks/target/bouquet/'),
    (T('Preferences'),'/globaleaks/target/preferences/'==URL(), '/globaleaks/target/preferences/'),
]

response.menu_admin = [
    (T('Receivers'),'/globaleaks/admin/targets/display'==URL(), '/globaleaks/admin/targets/display'),
#    (T('Groups'),'/globaleaks/admin/targetgroups'==URL(),'/globaleaks/admin/targetgroups'),
#    (T('Globalview'),'/globaleaks/target/view'==URL(), '/globaleaks/target/view'),
    (T('Config'),'/globaleaks/admin/config'==URL(), '/globaleaks/admin/config'),
    (T('Logout'),'/globaleaks/default/user/logout'==URL(), '/globaleaks/default/user/logout'),
    (T('Password'),'/globaleaks/default/user/change_password'==URL(), '/globaleaks/default/user/change_password'),
]
