# coding: utf8
# try something like

@auth.requires_login()
def index():
    return dict(message="hello from admin.py")

@auth.requires_login()
def targets():

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
def groups():
    tlist = None

    if(request.vars.edit and request.vars.edit.startswith("delete")):
        gl.delete_target(request.vars.edit.split(".")[1])

    if(request.vars.edit and request.vars.edit.startswith("edit")):
        pass

    form_content = (Field('Name', requires=IS_NOT_EMPTY()),
                    Field('Description'),
                    Field('Tags')
                   )

    form = SQLFORM.factory(*form_content)

    if "display" in request.args and not request.vars:
        tlist = TargetList()
        return dict(form=None, list=True, groups=tlist.list)

    if form.accepts(request.vars, session):
        # Build group target list with posted data
        tlist = TargetList(request.vars)
        return dict(form=form, list=True, groups=tlist.list)

    return dict(form=form, list=False, targets=None)



@auth.requires_login()
def config():
    response.flash = ("Welcome to the Globaleaks new wizard application")

    mail_form = FORM(TABLE(
            "foobar", TR(INPUT(_type='submit'))
            ))
    auth_form = FORM(TABLE(
            "verification",
            TR(INPUT(_type='submit'))
            ))

    global_form = FORM(TABLE(
        TR("title", INPUT(_name='title', _type='text',
                          _value=settings.globals.title)),
        TR("subtitle", INPUT(_name='subtitle', _type='text',
                             _value=settings.globals.subtitle)),
        TR("author", INPUT(_name='author', _type='text',
                           _value=settings.globals.author)),
        TR("author_email", INPUT(_name='author_email', _type='text',
                          _value=settings.globals.author_email)),

        TR(INPUT(_type='submit'))
    ))

    if global_form.accepts(request.vars, keepvalues=True):
        for var in global_form.vars:
            value = getattr(global_form.vars, var)
            setattr(settings.globals, var, value)

    if auth_form.accepts(request.vars, keepvalues=True):
        return str(dir(db))
    if mail_form.accepts(request.vars, session):
        return 'accepting mail'

    return dict(settings=settings,
                global_form=global_form,
                mail_form=mail_form,
                auth_form=auth_form)

@auth.requires_login()
def wizard():
    """
    Wizard page should be avaible only on startup, and provide with a cool
    graphical interface a configuration wizard.
        {{{ import cfg file }}}
      step #1:
        Node description, i.e. title and subtitle
      step #2:
        Supported output: mail, aws?
        (mail is the only options supported now.)
      step #3 {>>>skip}
        Tulip settings: expiration date, maximum access and so on.
      step #4: {>>>skip}
        Advanced configs: author email, layout theme, keywords
      step #5: {{>>>skip}}
        Create first grups
    """

    import_form = FORM(TR(INPUT(_name="imp_url", _type="url"),
                          "\tor\t",
                          INPUT(_name="imp_file", _type="file")),
                      )

    step1_form = FORM(TABLE(
        TR("Leak author", INPUT(_name= "author", _type="text",
            _value=settings.globals.author)),
        TR("Leak title", INPUT(_name="title", _type="text",
            _value=settings.globals.title)),
        TR("Leak description", INPUT(_name="subtitle", _type="text",
            _value=settings.globals.subtitle))
        ))

    step2_form = FORM(TABLE(
        TR("E-Mail Messages", INPUT(_name="mail", _type="checkbox", _value=True)),
        TR("SMS Messages", INPUT(_name="SMS", _type="checkbox", _value=True))
        ))

    step3_form = None
    step4_form = None
    step5_form = None

    return dict(import_form=import_form, step1=step1_form, step2=step2_form,
                step3=step3_form, step4=step4_form, step5=step5_form)

