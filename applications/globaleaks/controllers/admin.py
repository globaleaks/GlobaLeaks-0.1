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
            TR("server", INPUT(_name="server", _type="text")),
            TR("sender", INPUT(_name="sender", _type="text")),
            TR("login", INPUT(_name="login", _type="text")),
            TR(INPUT(_type="submit"))
            ))
    auth_form = FORM(TABLE(
            TR("verification", INPUT(_name="registration_requires_verification",
                                     _type="text",
                                     _value=settings.auth.registration_requires_verification)),
            TR("approval" , INPUT(_name="registration_requires_approval",
                                  _type="text",
                                  _value=settings.auth.registration_requires_approval)),
            TR(INPUT(_type="submit"))
            ))

    global_form = FORM(TABLE(
            TR("title", INPUT(_name='title', _type='text',
                              _value=settings.globals.title)),
            TR("subtitle", INPUT(_name='subtitle', _type='text',
                                 _value=settings.globals.subtitle)),
            TR("author", INPUT(_name='author', _type='text',
                               _value=settings.globals.author)),
            TR("author email", INPUT(_name='author_email', _type='text',
                                     _value=settings.globals.author_email)),
            TR(INPUT(_type="sumbit"))
    ))

    if global_form.accepts(request.vars, keepvalues=True):
        for var in global_form.vars:
            value = getattr(global_form.vars, var)
            setattr(settings.globals, var, value)

    if auth_form.accepts(request.vars, keepvalues=True):
        for var in auth_form.vars:
            value = getarre(auth_form.vars, var)
            setattr(settings.auth, var, value)
        # XXX: temporary added commit, there should be a class in config.py
        db.commit()
    if mail_form.accepts(request.vars, keepvalue=True):
        for var in mail_form.vars:
            value = getattr(auth.form.vars, var)
            setattr(settings.mail, var, value)
        # XXX: same as above.
        db.commit()

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

    step3_form = FORM(TABLE(
        TR("Expiration Date", INPUT(_name="expire", _type="text",
                                    _value=settings.tulip.expire)),
        TR("Maximum Access", INPUT(_name="max_access", _type="int",
                                   _value=settings.tulip.max_access))
        ))

    step4_form = FORM(TABLE(
        TR("Author Email", INPUT(_name="author_email", _type="email",
                                 _value=settings.globals.author_email)),
        TR("Layout Theme", INPUT(_name="layout_theme", _type="text",
                                 _value=settings.globals.layout_theme)),
        TR("HTML Keyword", INPUT(_name="html_keyword", _type="text",
                                _value=settings.globals.html_keyword))
        ))


    # set up here various groups: one group form + button "add group"
    step5_form = None

    return dict(import_form=import_form,
                step1=step1_form, step2=step2_form, step3=step3_form,
                step4=step4_form, step5=step5_form)

