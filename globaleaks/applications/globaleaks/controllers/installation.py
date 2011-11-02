#coding: utf-8
"""
This controller module contains every controller that the target can use
to edits its settings. (E.g.: Unsubscribe from a GL node)
"""

def index():
    """
    This view is like a tulip: reachable only by a personal secret,
    stored in db.target.url
    """

    form_password = (Field('new_passphrase', requires=IS_NOT_EMPTY()),
                     Field('recovery'),
                     Field('new_gpg'),
                    )
    password_info = SQLFORM.factory(*form_password, table_name="pass_update")

    if password_info.accepts(request.vars, session):
        response_t += "password accepted "
        print "password accepted"

    if not request.args:
        subscribe_form = SQLFORM.factory(
                            Field('Name', requires=IS_NOT_EMPTY()),
                            Field('Email', requires=IS_NOT_EMPTY()),
                            Field('Description', 'text',
                                  requires=IS_NOT_EMPTY())
                         )
        if subscribe_form.accepts(request.vars, session):
            return dict(message="Not implemented!", subscribe=None)

        return dict(message="Here you can subscribe as a target",
                    subscribe=subscribe_form)


#if db.auth_user:
#    if not db(db.auth_user.email=="node@globaleaks.org").select().first():
#        db.auth_user.insert(
#            first_name="Globaleaks node administrator",
#            last_name="Globaleaks",
#            email="node@globaleaks.org",
#            password=db.auth_user.password.validate("testing")[0])
#        logger.info("First launch of GlobaLeaks, creating node administrator!")
#        db.commit()
