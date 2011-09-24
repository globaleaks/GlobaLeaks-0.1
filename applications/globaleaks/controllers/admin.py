# coding: utf8
# try something like

@auth.requires_login()
def index():
    return dict(message="hello from admin.py")

@auth.requires_login()
def targets():

    response.flash = "You are now the GlobaLeaks Node Maintainer"

    if(request.vars.edit and request.vars.edit.startswith("delete")):
        gl.delete_target(request.vars.edit.split(".")[1])

    if(request.vars.edit and request.vars.edit.startswith("edit")):
        pass

    form_content = (Field('Name', requires=IS_NOT_EMPTY()),
                    Field('Description', requires=IS_LENGTH(minsize=5,maxsize=50)),
                    Field('email', requires=[IS_EMAIL(), IS_NOT_IN_DB(db, db.target.url)])
                   )

    form = SQLFORM.factory(*form_content)

    targets = gl.get_targets("ANY")

    if "display" in request.args and not request.vars:
        return dict(form=None, list=True, targets=targets)

    if form.accepts(request.vars, session):
        c = request.vars
        gl.create_target(c.Name, "demo", c.Description, c.email, "demo", "demo target")
        targets = gl.get_targets("ANY")
        return dict(form=form, list=True, targets=targets)

    return dict(form=form, list=False, targets=targets)

@auth.requires_login()
def config():
    create_form = lambda: FORM(TABLE(
            TR("title", INPUT(_name='title', _type='text',
                              _value=settings.globals.title)),
            TR("subtitle", INPUT(_name='subtitle', _type='text',
                                 _value=settings.globals.subtitle)),
            TR("author", INPUT(_name='author', _type='text',
                               _value=settings.globals.author)),
            TR("title", INPUT(_name='author_email', _type='text',
                              _value=settings.globals.title)),

            TR(INPUT(_type='submit'))
          ))

    global_form = create_form()
    if global_form.accepts(request.vars):
        for var in global_form.vars:
            value = getattr(global_form.vars,  var)
            setattr(settings.globals, var,  value)
        global_form = create_form()
    #if auth_form.accepts(request.vars, session):
    #    return 'accepting auth'
    #if mail_form.accepts(request.vars, session):
    #    return 'accepting mail'


    response.flash = ("Welcome to the Globaleaks new wizard application, "
                      "please donate coffee")

    # XXX: also private form?
    mail_form = FORM(TABLE(
            "foobar", TR(INPUT(_type='submit'))
            ))
    auth_form = FORM(TABLE(
            "verification",
            TR(INPUT(_type='submit'))
            ))


    return dict(settings=settings,
                global_form=global_form,
                mail_form=mail_form,
                auth_form=auth_form)

@auth.requires_login()
def wizard():
    """
    Wizard page should be avaible only on startup, and provide with a cool
    graphical interface a configuration wizard.
    """

    return dict(message=None)

