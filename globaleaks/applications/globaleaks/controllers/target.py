#coding: utf-8
"""
This controller module contains every controller that the target can use
to edits its settings. (E.g.: Unsubscribe from a GL node)
"""

def index():
    return dict(message="hello from target.py")


def view():
    collectedUser = []
    targetList = db(db.target.status=="subscribed").select()
    for active_user in targetList:
        collectedUser.append(active_user)

    inactiveUser = []
    unsubscribedList = db(db.target.status=="unsubscribed").select()
    for inactive_user in unsubscribedList:
        inactiveUser.append(inactive_user)

    leakActive = []
    flowers = db().select(db.leak.ALL)
    for active_leak in flowers:
        leakActive.append(active_leak)

    groupsUsage = []
    groupList = db().select(db.targetgroup.ALL)
    for group in groupList:
        groupsUsage.append(group)

    # this require to be splitted because tulip are leak x target matrix
    tulipAvail = []
    tulipList = db().select(db.tulip.ALL)
    for singleT in tulipList:
        tulipAvail.append(singleT)

    return dict(active=collectedUser,
                inactive=inactiveUser,
                flowers=leakActive,
                groups=groupsUsage,
                tulips=tulipAvail)
    # nevah forget http://uiu.me/Nr9G.png


# this view is like a tulip: reachable only by a personal secret,
# stored in db.target.url
def personal():
    pass


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


def unsubscribe():
    if request.args:
        tulip_url = request.args[0]
    else:
        tulip_url = None

    try:
        tulip = Tulip(url=tulip_url)
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
