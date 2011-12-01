#coding: utf-8
"""
This controller module contains every controller that the target can use
to edits its settings. (E.g.: Unsubscribe from a GL node)
"""

def mandatory_setup():
    import os
    """
    This controller is called only at the first start of GlobaLeaks service
    """

    # mandatory: admin login/password and node name
    mandatory_input = (
                    Field('administrative_password', 'password',
                        requires = IS_LENGTH(minsize=8) ),
                    Field('confirm_password', 'password',
                        requires=IS_EQUAL_TO(request.vars.administrative_password, error_message="passwords do not match")),
                   )

    mandatory_form = SQLFORM.factory(*mandatory_input, table_name="mandatory")

    # handle the first connection
    if not mandatory_form.accepts(request.vars, session, keepvalues=True):
        return dict(configured=False, mandatory=mandatory_form)

    # handle the admin setup
    db.auth_user.insert(
        first_name="GlobaLeaks",
        last_name="node administrator",
        username=settings['globals'].node_admin_username, # default: 'admin'
        password=db.auth_user.password.validate(request.vars.administrative_password)[0]
    )
    logger.info("recorded node administrator password (login: %s)" % settings['globals'].node_admin_username)
    db.commit()

    settings.globals.commit()

    # this is a MANDATORY STEP, therefore HERE is added the default group
    if settings['globals'].default_group:
        gl.create_targetgroup(settings['globals'].default_group, "Default receiver group", None)

    print "mandatory settings: saved"
    return dict(configured=True)

