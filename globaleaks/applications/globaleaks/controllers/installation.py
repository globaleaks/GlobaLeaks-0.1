#coding: utf-8
"""
This controller module contains every controller that the target can use
to edits its settings. (E.g.: Unsubscribe from a GL node)
"""
def record_mandatory(vars):
    import os

    # require a check
    db.auth_user.insert(
        first_name="GlobaLeaks",
        last_name="node administrator",
        username=settings['globals'].node_admin_username,
        password=db.auth_user.password.validate(vars.administrative_password)[0]
    )
    logger.info("recorded node administrator password (login: %s)" % settings['globals'].node_admin_username)
    db.commit()

    settings['globals'].node_admin_configured = True
    settings['globals'].email_server = vars.email_server
    settings['globals'].email_sender = vars.email_sender
    settings['globals'].title = vars.globaleaks_name

    settings.globals.commit()

    # this is a MANDATORY STEP, therefore HERE is added the default group
    if settings['globals'].default_group:
        gl.create_targetgroup(settings['globals'].default_group, "Default receiver group", None)

    print "mandatory settings: saved"

def record_required(vars):

    settings['globals'].headline = vars.headline
    settings['globals'].tulip_expire_days = vars.tulip_expire_days
    settings['globals'].tulip_max_download = vars.tulip_max_download
    settings['globals'].html_meta_keywords = vars.html_meta_keywords

    settings.globals.commit()

    print "required settings: saved"

def record_optional(vars):
    print "optional saved"

def configuration():
    """
    This controller is called only at the first start of GlobaLeaks service
    """

    # mandatory: admin login/password and node name
    mandatory_input = (
                    Field('email_server', requires=IS_NOT_EMPTY()),
                    Field('email_sender', requires=IS_NOT_EMPTY()),
                    Field('globaleaks_name', requires=IS_NOT_EMPTY()),
                    Field('administrative_password', requires = [IS_NOT_EMPTY(), IS_STRONG(min=8)] ),
                    Field('confirm_password', requires=IS_EQUAL_TO(request.vars.administrative_password, error_message="passwords do not match")),
                   )
    # check: something don't work with javascript checks apply to special char
    # Field('administrative_password', requires = [IS_NOT_EMPTY(), IS_STRONG(min=8, special=2, upper=2)] ),

    mandatory_form = SQLFORM.factory(*mandatory_input, table_name="mandatory")
    # check: why is not working keepvalues ?

    if mandatory_form.accepts(request.vars, session, keepvalues=True):
        record_mandatory(request.vars)

    # required
    required_input = (
                    Field('headline', requires=IS_NOT_EMPTY()),
                    Field('tulip_expire_days', requires=IS_NOT_EMPTY()),
                    Field('tulip_max_download', requires=IS_NOT_EMPTY()),
                    Field('html_meta_keywords', requires=IS_NOT_EMPTY()),
                   )
    required_form = SQLFORM.factory(*required_input, table_name="required")

    if required_form.accepts(request.vars, session, keepvalues=True):
        record_required(request.vars)

    # optional
    optional_input = (
                    Field('some_shit'),
                   )
    optional_form = SQLFORM.factory(*optional_input, table_name="optional")

    if optional_form.accepts(request.vars, session, keepvalues=True):
        record_optional(request.vars)

    return dict(mandatory=mandatory_form, required=required_form, optional=optional_form)

