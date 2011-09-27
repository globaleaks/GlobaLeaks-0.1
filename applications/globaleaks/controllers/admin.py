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

    all_targets = []
    result = {}
    for row in db().select(db.targetgroup.ALL):
        result[row.id] = {}
        result[row.id]["data"] = dict(row)
        result[row.id]["members"] = []

    # retrieving groups data from db
    for row in db().select(db.target.ALL):
        target_data = dict(row)
        all_targets.append(target_data)
        if not row.groups:
            continue
        groups = pickle.loads(row.groups)
        for group in groups:
            group_q = db(db.targetgroup.id==int(group)).select().first()
            if not group_q:
                continue
            group_data = dict(group_q)
            if not result.has_key(group_q.id):
                result[group_q.id] = {}
            if not result[group_q.id].has_key("data"):
                result[group_q.id]["data"] = dict(group_q)
            try:
                result[group_q.id]["members"].append(target_data)
            except KeyError:
                result[group_q.id]["members"] = [target_data]

    return dict(form=form, list=False, targets=None,
                all_targets=all_targets, targetgroups=result)

@auth.requires_login()
def group_create():
    """
    Receives parameters "name", "desc", and "tags" from POST.
    Creates a new target group with the specified parameters
    """
    # XXX fix to POST! get only for test
    try:
        name = request.get_vars["name"]
        desc = request.get_vars["desc"]
        tags = request.get_vars["tags"]
    except KeyError:
        return response.json({'success':'false'})
    else:
        db.targetgroup.insert(name=name,
                              desc=desc,
                              tags=tags)
        db.commit()
        return response.json({'success':'true'})

@auth.requires_login()
def group_add():
    """
    Receives parameters "target" and "group" from POST.
    Adds taget to group.
    """
    # XXX fix to POST! get only for test
    try:
        target_id = request.get_vars["target"]
        group_id = request.get_vars["group"]
    except KeyError:
        pass
    else:
        target_row = db(db.target.id==target_id).select().first()
        group_row = db(db.targetgroup.id==group_id).select().first()

        if target_row is not None and group_row is not None:
            groups_p = target_row.groups
            if not groups_p:
                groups_p = pickle.dumps(set([group_id]))
            else:
                tmp = pickle.loads(groups_p)
                tmp.add(group_id)
                groups_p = pickle.dumps(tmp)
            db(db.target.id==target_id).update(groups=groups_p)
            db.commit()
            return response.json({'success':'true'})

    return response.json({'success':'false'})


@auth.requires_login()
def group_remove():
    """
    Receives parameters "target" and "group" from POST.
    Removes taget from group.
    """
    # XXX fix to POST! get only for test
    try:
        target_id = request.get_vars["target"]
        group_id = request.get_vars["group"]
    except KeyError:
        pass
    else:
        target_row = db(db.target.id==target_id).select().first()
        group_row = db(db.targetgroup.id==group_id).select().first()

        if target_row is not None and group_row is not None:
            groups_p = target_row.groups
            if groups_p:
                tmp = pickle.loads(groups_p)
                try:
                    tmp.remove(group_id)
                except KeyError:
                    pass
                else:
                    groups_p = pickle.dumps(tmp)
                    db(db.target.id==target_id).update(groups=groups_p)
                    db.commit()
            return response.json({'success':'true'})

    return response.json({'success':'false'})


@auth.requires_login()
def config():
    response.flash = ("Welcome to the Globaleaks new wizard application")

    mail_form = FORM(TABLE(
            TR("foobar", INPUT(_name="foo"))
            ))
    auth_form = FORM(TABLE(
            TR("verification", INPUT(_name="registration_requires_verification",
                                     _type="text",
                                     _value=settings.auth.registration_requires_verification)),
            TR("approval" , INPUT(_name="registration_requires_approval",
                                      _type="text",
                                      _value=settings.auth.registration_requires_approval))
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

    return dict(import_form=import_form, step1=step1_form, step2=step2_form,
                step3=step3_form, step4=step4_form, step5=step5_form)

