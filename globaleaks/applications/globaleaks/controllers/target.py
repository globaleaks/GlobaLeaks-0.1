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
def debugview():
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

@configuration_required
def bouquet():
    """
    This page is indexed by an uniq identifier by the receiver, and shows
    all him accessible Tulips, its the page where she/he could change their
    preferences
    """
    if request and request.args:
        target_url = request.args[0]
    else:
        return dict(err="Tulip index not supplied")

    # maybe better continue to devel Target class in datamodel.py
    # XXX here security issue to think about, create_target involved.
    # X&Y challenge response required

    try:
        tulip = Tulip(url=target_url)
    except:
        return dict(err="Invalid Tulip")

    receiver_row = db(db.target.id==tulip.target).select()
    
    # this require to be splitted because tulip are leak x target matrix
    bouquet_list = []
    tulip_list = db(db.tulip.target_id==receiver_row[0].id).select()
    for single_t in tulip_list:
        bouquet_list.append(single_t)

    return dict(err=False,
                bouquet=bouquet_list,
                target=receiver_row[0])
