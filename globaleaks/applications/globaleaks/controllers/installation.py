#coding: utf-8
"""
This controller module contains every controller that the target can use
to edits its settings. (E.g.: Unsubscribe from a GL node)
"""
def record_mandatory(vars):
    import os
    print vars
    if db.auth_user:
        db.auth_user.insert(
            first_name="GlobaLeaks",
            last_name="Node",
            email="node@globaleaks.org",
            password=db.auth_user.password.validate(vars.administrative_password)[0])
        logger.info("First launch of GlobaLeaks, creating node administrator!")
        db.commit()
    install_ok_name = 'installstorage/.installed'

    with open(os.path.join(os.getcwd(), install_ok_name), 'w') as fp:
        fp.write('yep')

    print "mandatory saved"

def record_required(vars):
    print "required saved"

def record_optional(vars):
    print "optional saved"

def configuration():
    """
    This controller is called only at the first start of GlobaLeaks service
    """

    # mandatory: admin login/password and node name
    mandatory_input = (
                    Field('administrative_password', requires=IS_NOT_EMPTY()),
                    Field('globaleaks_name', requires=IS_NOT_EMPTY()),
                   )

    mandatory_form = SQLFORM.factory(*mandatory_input, table_name="mandatory")

    if mandatory_form.accepts(request.vars, session):
        record_mandatory(request.vars)

    # required
    required_input = (
                    Field('headline', requires=IS_NOT_EMPTY()),
                    Field('tulip_expire_days', requires=IS_NOT_EMPTY()),
                    Field('tulip_max_download', requires=IS_NOT_EMPTY()),
                    Field('html_meta_keywords', requires=IS_NOT_EMPTY()),
                   )
    required_form = SQLFORM.factory(*required_input, table_name="required")

    if required_form.accepts(request.vars, session):
        record_required(request.vars)

    # optional
    optional_input = (
                    Field('some_shit'),
                   )
    optional_form = SQLFORM.factory(*optional_input, table_name="optional")

    if optional_form.accepts(request.vars, session):
        record_optional(request.vars)

    return dict(mandatory=mandatory_form, required=required_form, optional=optional_form)

