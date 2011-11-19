#coding: utf-8
"""
This controller module contains every controller that the target can use
to edits its settings. (E.g.: Unsubscribe from a GL node)
"""

@configuration_required
def index():
    return dict(message="hello from target.py")

@configuration_required
@auth.requires_login()
def view():
    collected_user = []
    target_list = db(db.target.status=="subscribed").select()
    for active_user in target_list:
        collected_user.append(active_user)

    inactive_user = []
    unsubscribed_list = db(db.target.status=="unsubscribed").select()
    for user in unsubscribed_list:
        inactive_user.append(user)

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
                inactive=inactive_user,
                flowers=leak_active,
                groups=groups_usage,
                tulips=tulip_avail)
    # nevah forget http://uiu.me/Nr9G.png

@configuration_required
@auth.requires(auth.has_membership('targets'))
def receiver():
    """
    This view is like a tulip: reachable only by a personal secret,
    stored in db.target.url
    """
    import hashlib

    if not request or not request.post_vars or \
       not request.post_vars["targetid"]:
        return dict(err=False)

    try:
        passphrase = request.post_vars["targetid"]
        target_url = hashlib.sha256(passphrase).hexdigest()
        redirect("/globaleaks/target/bouquet/" + target_url)
    except KeyError:
        return dict(err=True)

@configuration_required
@auth.requires(auth.has_membership('targets'))
def bouquet():
    """
    This page is indexed by an uniq identifier by the receiver, and shows
    all him accessible Tulips, its the page where she/he could change their
    preferences
    """
    if request and request.args:
        target_url = request.args[0]
    else:
        return dict(err="password not supply")

    # maybe better continue to devel Target class in datamodel.py
    # XXX here security issue to think about, create_target involved.
    # X&Y challenge response required

    receiver_row = db(db.target.hashpass==target_url).select()
    if len(receiver_row) == 0:
        return dict(err="invald password supply")
    if len(receiver_row) > 1:
        return dict(err="temporary fault: collision detected, two target"
                        "with the same password")

    # fixme: this bug depends by the actual bad auth type

    # addiction information could be present in the POST
    # here are treated the configuration option, and returned in the variable
    # "response"
    response_t = ""

    form_password = (Field('new_passphrase', requires=IS_NOT_EMPTY()),
                     Field('recovery'),
                     Field('new_gpg'),
                    )
    password_info = SQLFORM.factory(*form_password, table_name="pass_update")

    if password_info.accepts(request.vars, session):
        response_t += "password accepted "

    form_receiving = (  Field('new_server', requires=IS_NOT_EMPTY()),
                        Field('scp_enable_copy'),
                        Field('new_key', requires=IS_NOT_EMPTY()),
                    )
    receiving_info = SQLFORM.factory(*form_receiving,
                                     table_name="receiving_update")

    if receiving_info.accepts(request.vars, session):
        response_t += "receiving update accepted "

    # the contact-type required to be updated
    form_contact = (  Field('new_contact'), Field('new_email'), )
    contact_info = SQLFORM.factory(*form_contact, table_name="contact_update")

    if contact_info.accepts(request.vars, session):
        response_t += "contact update accepted "

    # this require to be splitted because tulip are leak x target matrix
    bouquet_list = []
    tulip_list = db(db.tulip.target_id==receiver_row[0].id).select()
    for single_t in tulip_list:
        bouquet_list.append(single_t)

    return dict(err=False,
                bouquet=bouquet_list,
                target=receiver_row[0],
                answer=response_t)

@configuration_required
@auth.requires(auth.has_membership('targets'))
def subscribe():
    if not request.args:
        subscribe_form = SQLFORM.factory(
                            Field('Name', requires=IS_NOT_EMPTY()),
                            Field('Email', requires=IS_NOT_EMPTY()),
                            Field('Description', 'text',
                                  requires=IS_NOT_EMPTY())
                         )
        if subscribe_form.accepts(request.vars, session):
            return dict(message="Not implemented!", subscribe=None)

        return dict(message="Here you can subscribe as a target",
                    subscribe=subscribe_form)

    if request.args:
        tulip_url = request.args[0]
    else:
        tulip_url = None

    try:
        tulip = Tulip(url=tulip_url)
    # XXX specify exception
    except:
        return dict(message="Error!", subscribe=None)

    if not tulip_url or tulip.target == "0":
        return dict(message="Error!", subscribe=None)

    else:
        target = db(db.target.id==tulip.target).select().first()

        if not target:
            return dict(message="Error!", subscribe=None)

        if target.status == "subscribed":
            return dict(message="already subscribed", subscribe=None)

        else:
            db.target[tulip.target].update_record(status="subscribed")
            return dict(message="subscribed", subscribe=None)

    return dict(message="this is logically impossible", subscribe=None)

@configuration_required
@auth.requires(auth.has_membership('targets'))
def unsubscribe():
    if request.args:
        tulip_url = request.args[0]
    else:
        tulip_url = None

    try:
        tulip = Tulip(url=tulip_url)
    # XXX specify exception
    except:
        return dict(message="Error!")

    if not tulip_url or tulip.target == "0":
        return dict(message="Error!")

    else:
        target = db(db.target.id==tulip.target).select().first()

        if not target:
            return dict(message="Error!")

        if target.status == "unsubscribed":
            return dict(message="already unsubscribed")

        else:
            db.target[tulip.target].update_record(status="unsubscribed")
            return dict(message="unsubscribed")

    return dict(message="this is logically impossible")
