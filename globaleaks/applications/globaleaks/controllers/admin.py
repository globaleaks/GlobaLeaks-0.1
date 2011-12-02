# coding: utf8
"""
Controller module for the admin interface.
Contains every controller that must run with admin privileges.

Every controller in this file must have the @auth.requires_login() decorator
"""
from shutil import copyfile
import hashlib
from config import projroot, cfgfile, copyform

session.admin = True

@auth.requires_login()
def index():
    """
    Controller for admin index page
    """
    session.admin = True
    return dict(message="hello from admin.py")

def obtain_secret(input_secret):
    if not input_secret:
        ret = randomizer.generate_target_passphrase()[0]
        return None
    else:
        return input_secret

@auth.requires_login()
def nodeprivacy():
    """
    Controller for page that let the admin to configure privacy settings
    """
    if request.vars.edit:
        if request.vars.edit == "start" :
            settings.globals.hiddenservice = "true"
            settings.globals.commit()
            tor_hs.start()
        elif request.vars.edit == "stop":
            settings.globals.hiddenservice = "false"
            settings.globals.commit()
            tor_hs.stop()

    return dict()

@auth.requires_login()
def targets():
    """
    Controller for page that lets the admin to create new targets
    """
    crud.settings.detect_record_change = False
    if (request.vars.edit and request.vars.edit.startswith("delete")):
        gl.delete_target(request.vars.edit.split(".")[1])
    
    # it's possible delete via ajax and add via POST
    if (request.vars.edit and request.vars.edit.startswith("edit")):
        update_form = crud.update(db.target, request.vars.edit.split(".")[1])
        return dict(form=update_form)

    # is hardcoded email, supposing that, at the moment, every subscription
    # happen with email only. in the future, other kind of contacts could be
    # setup from the start.
    form_content = (Field('Name', requires=IS_NOT_EMPTY()),
                    Field('Description',
                          requires=IS_LENGTH(minsize=5, maxsize=50)),
                    Field('contact', requires=[IS_EMAIL(),
                          IS_NOT_IN_DB(db, db.target.contact)]),
                    Field('passphrase'), Field('could_delete', 'boolean'), #extern the text in view
                   )

    form = SQLFORM.factory(*form_content)

    targets_list = gl.get_targets(None)

    # provide display only, whan controller is called as targets/display
    if "display" in request.args and not request.vars:
        return dict(form=None, list_only=True, targets=targets_list,
                    default_group=settings['globals'].default_group, edit=None)

    if form.accepts(request.vars, session):
        req = request.vars
        passphrase = obtain_secret(req.passphrase)

        # here some mistake happen, I wish that now has been fixed and not augmented

        if not passphrase:
            passphrase = randomizer.generate_target_passphrase()[0]

        target_id = gl.create_target(req.Name, None, req.Description,
                                     req.contact, req.could_delete,
                                     hashlib.sha256(passphrase).hexdigest(),
                                    "subscribed")

        target = db.auth_user.insert(first_name=req.Name,
                                     last_name="",
                                     username=target_id,
                                     email=req.contact,
                                     password=db.auth_user.password.validate(passphrase)[0]
                                     )
        auth.add_membership(auth.id_group("targets"), target)

        targets_list = gl.get_targets("ANY")

    # switch list_only=None if, in the adding interface, the list has not to be showed
    return dict(form=form, list_only=None, targets=targets_list,
                default_group=settings['globals'].default_group, edit=True)

@auth.requires_login()
def targetgroups():
    """
    Controller for the targets management page.
    It creates two forms, one for creating a new target and one for
    creating a new group.
    """
    form_content_group = (Field('Name', requires=[IS_NOT_EMPTY(),
                                IS_NOT_IN_DB(db, db.targetgroup.name)]),
                          Field('Description'),
                          Field('Tags'),
                         )
    form_group = SQLFORM.factory(*form_content_group, table_name="form_group")

    if form_group.accepts(request.vars, session):
        # Build group target list with posted data
        TargetList(request.vars)

    form_content_target = (Field('Name', requires=IS_NOT_EMPTY()),
                    Field('Description', requires=IS_LENGTH(minsize=5,
                                                            maxsize=50)),
                    Field('contact',
                          requires=[IS_EMAIL(),
                                    IS_NOT_IN_DB(db, db.target.contact)]),
                    Field('passphrase'), Field('coulddelete', 'boolean'), # extern in view the text
                   )

    form_target = SQLFORM.factory(*form_content_target,
                                  table_name="form_target")

    if form_target.accepts(request.vars, session):
        req = request.vars
        passphrase = obtain_secret(req.passphrase)

        if not passphrase:
            target_id = gl.create_target(req.Name, None, req.Description, req.contact, req.coulddelete,
                             None, "subscribed")
            passphrase = randomizer.generate_target_passphrase()[0]

        else:
            target_id = gl.create_target(req.Name, None, req.Description, req.contact, req.coulddelete,
                             hashlib.sha256(passphrase).hexdigest(), "subscribed")


        target = db.auth_user.insert(first_name=req.Name,
                                     last_name="",
                                     username=target_id,
                                     email=req.contact,
                                     password=db.auth_user.password.validate(passphrase)[0]
                                     )
        auth.add_membership(auth.id_group("targets"), target)

    all_targets = gl.get_targets(None)
    targetgroups_list = gl.get_targetgroups()

    return dict(form_target=form_target, form_group=form_group,
                list=False, targets=None, all_targets=all_targets,
                targetgroups=targetgroups_list)

@auth.requires_login()
def group_create():
    """
    Receives parameters "name", "desc", and "tags" from POST.
    Creates a new target group with the specified parameters
    """
    try:
        name = request.post_vars["name"]
        desc = request.post_vars["desc"]
        tags = request.post_vars["tags"]
    except KeyError:
        return response.json({'success': 'false'})
    else:
        gl.create_targetgroup(name, desc, tags)
        return response.json({'success': 'true'})


@auth.requires_login()
def group_delete():
    """
    Receives parameter "group" with the group id from POST.
    Deletes the target group with the specified parameters
    """
    try:
        group_id = request.post_vars["group"]
    except KeyError:
        pass
    else:
        result = gl.delete_targetgroup(group_id)
        if result:
            return response.json({'success': 'true'})
    return response.json({'success': 'false'})


@auth.requires_login()
def group_rename():
    """
    Receives the parameter "group" with the group id and "name"
    with the new name for the group from POST.
    Renames the group with the new name.
    """
    try:
        group_id = request.post_vars["group"]
        name = request.post_vars["name"]
    except KeyError:
        pass
    else:
        result = gl.update_targetgroup(group_id, name=name)
        if result:
            return response.json({'success': 'true'})
    return response.json({'success': 'false'})


#@auth.requires_login()
def group_desc():
    """
    Receives the parameter "group" with the group id and "desc"
    with the new description for the group from POST.
    Updates the group desc
    """
    try:
        group_id = request.post_vars["group"]
        desc = request.post_vars["desc"]
    except KeyError:
        pass
    else:
        result = gl.update_targetgroup(group_id, desc=desc)
        if result:
            return response.json({'success': 'true'})
    return response.json({'success': 'false'})


@auth.requires_login()
def group_tags():
    """
    Receives the parameter "group" with the group id and "tags"
    with the new tags for the group from POST.
    Updates the group tags.
    """
    try:
        group_id = request.post_vars["group"]
        tags = request.post_vars["tags"]
    except KeyError:
        pass
    else:
        result = gl.update_targetgroup(group_id, tags=tags)
        if result:
            return response.json({'success': 'true'})
    return response.json({'success': 'false'})


@auth.requires_login()
def target_add():
    """
    Receives parameters "target" and "group" from POST.
    Adds taget to group.
    """
    try:
        target_id = request.post_vars["target"]
        group_id = request.post_vars["group"]
    except KeyError:
        pass

    result = gl.add_to_targetgroup(target_id, group_id)

    if result:
        return response.json({'success': 'true'})

    return response.json({'success': 'false'})


@auth.requires_login()
def target_remove():
    """
    Receives parameters "target" and "group" from POST.
    Removes taget from group.
    """
    try:
        target_id = request.post_vars["target"]
        group_id = request.post_vars["group"]
    except KeyError:
        pass
    else:
        result = gl.remove_from_targetgroup(target_id, group_id)
        if result:
            return response.json({'success': 'true'})
    return response.json({'success': 'false'})

@auth.requires_login()
def target_delete():
    try:
        target_id = request.post_vars["target"]
    except KeyError:
        pass
    else:
        result = gl.delete_target(target_id)
        if result:
            return response.json({'success': 'true'})
    return response.json({'success': 'false'})
