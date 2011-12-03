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

@auth.requires_login()
def targets():
    """
    Controller for page that lets the admin to create new targets
    """
    # first operation is get the target list, because every dict() returned 
    # will need it
    targets_list = gl.get_targets(None)

    crud.settings.detect_record_change = False
    if (request.vars.edit and request.vars.edit.startswith("delete")):
        gl.delete_target(request.vars.edit.split(".")[1])
        # update the list
        targets_list = gl.get_targets(None)
    
    # it's possible delete via ajax and add via POST
    if (request.vars.edit and request.vars.edit.startswith("edit")):

        update_form = crud.update(db.target, request.vars.edit.split(".")[1])

        return dict(targets=targets_list, default_group=settings['globals'].default_group, 
                    form=update_form, edit=True)

    # is hardcoded email, supposing that, at the moment, every subscription
    # happen with email only. in the future, other kind of contacts can be
    # setup from the start.
    form_content = (Field('Name', requires=IS_NOT_EMPTY()),
                    Field('Description',
                          requires=IS_LENGTH(minsize=5, maxsize=50)),
                    Field('contact', requires=[IS_EMAIL(),
                          IS_NOT_IN_DB(db, db.target.contact)]),
                    Field('can_delete', 'boolean'), #extern the text in view
                   )

    add_form = SQLFORM.factory(*form_content)

    # provide display only, when controller is called as targets/display
    if "display" in request.args and not request.vars:
        return dict(form=None, list_only=True, targets=targets_list,
                    default_group=settings['globals'].default_group, edit=None)
    # default: you don't call display, and the list is show anyway.

    if add_form.accepts(request.vars, session):
        req = request.vars

        # here some mistake happen, I wish that now has been fixed and not augmented

        target_id = gl.create_target(req.Name, None, req.Description,
                                     req.contact, req.can_delete)

        target = db.auth_user.insert(first_name=req.Name,
                                     last_name="",
                                     username=target_id,
                                     email=req.contact)
        auth.add_membership(auth.id_group("targets"), target)

        targets_list = gl.get_targets("ANY")

    # switch list_only=None if, in the adding interface, the list has not to be showed
    return dict(form=add_form, list_only=None, targets=targets_list,
                default_group=settings['globals'].default_group, edit=None)

@configuration_required
@auth.requires_login()
def statistics():
    collected_user = []
    target_list = db().select(db.target.ALL)
    for active_user in target_list:
        collected_user.append(active_user)

    leak_active = []
    flowers = db().select(db.leak.ALL)
    for leak in flowers:
        leak_active.append(leak)

    groups_usage = []
    group_list = db().select(db.targetgroup.ALL)
    for group in group_list:
        groups_usage.append(group)

    # this require to be splitted because tulip are leak x target matrix
    tulip_avail = []
    tulip_list = db().select(db.tulip.ALL)
    for single_t in tulip_list:
        tulip_avail.append(single_t)

    return dict(active=collected_user,
                flowers=leak_active,
                groups=groups_usage,
                tulips=tulip_avail)
    # nevah forget http://uiu.me/Nr9G.png


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
        gl.delete_tulips_by_target(target_id)
        # delete_target remove simply the target
        result = gl.delete_target(target_id)
        if result:
            return response.json({'success': 'true'})
    return response.json({'success': 'false'})
