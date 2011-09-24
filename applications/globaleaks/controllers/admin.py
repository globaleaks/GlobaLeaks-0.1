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
    response.flash = ("Welcome to the Globaleaks new wizard application, "
                      "please donate coffee")

    form = FORM(TABLE(
                TR(INPUT(_name='migrate', _type='checkbox')),
                TR(INPUT(_name='name', _type='submit', requires=IS_NOT_EMPTY())),
                TR(INPUT(_name='email', _type='email')),
                TR(INPUT(_name='tutle', _type='submit')),
                TR(INPUT(_type='submit'))
                ))
    if form.accepts(request.vars, session):
        return True

    return dict(settings=settings,
               form=form)

@auth.requires_login()
def wizard():
    """
    Wizard page should be avaible only on startup, and provide with a cool
    graphical interface a configuration wizard.
    """
    return dict(message=None)

