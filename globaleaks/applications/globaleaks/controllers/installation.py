"""
This controller is called only during the Node setup
"""

@auth.requires(auth.requires_login() or not configuration_required)
def password_setup():
    import os
    """
    This controller is the second mandatory step inside the procedure setup, is called after the
    requested reboot, and here the hidden service name can be accessess and shown to the admin.
    Here the admin can setup various information, saved in the config file (useful to avoid terminal
    editing)
    """

    # mandatory: admin login/password and node name
    mandatory_input = (Field('administrative_password', 'password', requires = IS_LENGTH(minsize=8) ),
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
        username=settings.globals.node_admin_username, # default: 'admin'
        password=db.auth_user.password.validate(request.vars.administrative_password)[0]
    )

    logger.info("recorded node administrator password (login: %s)" % settings['globals'].node_admin_username)
    db.commit()

    # this is a MANDATORY STEP, therefore HERE is added the default group
    if settings.globals.default_group:
        gl.create_targetgroup(settings.globals.default_group, "Default receiver group", None)

    settings.globals.under_installation = False;
    settings.globals.commit()

    return dict(configured=True, mandatory=mandatory_form)
