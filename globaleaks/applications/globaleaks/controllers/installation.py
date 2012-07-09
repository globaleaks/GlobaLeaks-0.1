"""
This controller is called only during the Node setup
"""

@auth.requires(auth.requires_login() or not configuration_required)
def start_setup():
    import os
    """
    This controller is called only at the first start of GlobaLeaks service
    """

    start_input = ( Field('node_name', requires=IS_NOT_EMPTY()),
                    Field('title', requires=IS_NOT_EMPTY()),
                    Field('subtitle', requires=IS_NOT_EMPTY()),
                    Field('description', requires=IS_NOT_EMPTY()),
                    Field('page_author_name', requires=IS_NOT_EMPTY(), default='name in the meta keyword'),
                    Field('email_sender_appearance', requires=IS_NOT_EMPTY(), default='GlobaLeaks initiative <your@email.addr>'),
                    Field('email_auth', requires=IS_NOT_EMPTY(), default='username_or_email:password'),
                    Field('email_server', requires=IS_NOT_EMPTY(), default='server_host:server_port'),
                    Field('baseurl', default='used in the mail notification'), )

    start_form = SQLFORM.factory(*start_input, table_name="start")

    if not start_form.accepts(request.vars, session):
        return dict(configured=False, configuration_data=start_form)

    settings.globals.under_installation = True

    settings.globals.title = request.vars.title
    settings.globals.subtitle = request.vars.subtitle
    settings.globals.author = request.vars.page_author_name
    settings.globals.description = request.vars.description

    # check the PORT, if 25 is enable_ssl = False, else is True
    settings.globals.email_server = request.vars.email_server

    valuecheck = request.vars.email_server.split(':')
    # if not ":port" is provided, a default 25 is assumed
    if len(valuecheck) != 2 or int(valuecheck[1]) == 25:
        settings.globals.email_ssl = False
    else:
        settings.globals.email_ssl = True

    settings.globals.email_sender = request.vars.email_sender_appearance
    settings.globals.email_login = request.vars.email_auth
    settings.globals.baseurl = request.vars.baseurl

    settings.globals.commit()

    return dict(configured=True, configuration_data=start_form)

@auth.requires(auth.requires_login() or not configuration_required)
def virtual_setup():
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
		return dict(configured=False, mandatory=mandatory_form, hidden_service=settings.globals.hsurl[0:16])

    # handle the admin setup
    db.auth_user.insert(
        first_name="GlobaLeaks",
        last_name="node administrator",
        username=settings.globals.node_admin_username,
        password=db.auth_user.password.validate(request.vars.administrative_password)[0]
    )

    logger.info("recorded node administrator password (login: %s)" % settings['globals'].node_admin_username)
    db.commit()

    # this is a MANDATORY STEP, therefore HERE is added the default group
    if settings.globals.default_group:
        gl.create_targetgroup(settings.globals.default_group, "Default receiver group", None)

    """
    Trick: restore under_installation to True, to reset the HS and the GL config
    """
    settings.globals.under_installation = False;
    settings.globals.commit()

    return dict(configured=True, mandatory=mandatory_form)

@auth.requires(auth.requires_login() or not configuration_required)
def hidden_service_error():
    return dict(x=None)
