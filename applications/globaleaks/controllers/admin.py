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
                    Field('Description', 'text', requires=IS_LENGTH(minsize=5,maxsize=50)),
                    Field('email', requires=[IS_EMAIL(), IS_NOT_IN_DB(db, db.target.url)])
                   )
   
    form = SQLFORM.factory(*form_content)

    targets = gl.get_targets("ANY")
    
    if "display" in request.args and not request.vars:
        return dict(form=None, list=True, targets=targets)
    
    if form.accepts(request.vars, session):
        c = request.vars
        gl.create_target(c.Name, "demo", c.Description, c.email, "demo", "demo target")
        return dict(form=form, list=True, targets=targets)
 
    return dict(form=form, list=False, targets=targets)
