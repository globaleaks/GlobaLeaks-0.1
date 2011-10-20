#coding: utf-8
"""
This controller module contains every controller for accessing the tulip
from a target
"""


def index():
    import hashlib

    form = SQLFORM.factory(Field('Receipt', requires=IS_NOT_EMPTY()))

    if form.accepts(request.vars, session):
        l = request.vars

        # Make the tulip work well
        leak_number = l.Receipt.replace(' ', '')
        tulip_url = hashlib.sha256(leak_number).hexdigest()
        redirect("/tulip/" + tulip_url)

    redirect("/")


def access_increment(tulip):
    if tulip.accesses_counter:
        new_count = int(tulip.accesses_counter) + 1
        db.tulip[tulip.target].update_record(accesses_counter=new_count)
    else:
        db.tulip[tulip.target].update_record(accesses_counter=1)

    db.commit()

    if int(tulip.allowed_accesses) != 0 and \
       int(tulip.accesses_counter) > int(tulip.allowed_accesses):
        return True
    else:
        return False


# http://games.adultswim.com/robot-unicorn-attack-twitchy-online-game.html
def record_comment(comment_feedback, tulip):
    db.comment.insert(leak_id=tulip.get_leak().get_id(),
                      commenter_id=tulip.get_target(),
                      comment=comment_feedback)
    db.commit()

    if tulip.feedbacks_provided:
        new_count = int(tulip.feedbacks_provided) + 1
        db.tulip[tulip.id].update_record(feedbacks_provided=new_count)
    else:
        db.tulip[tulip.id].update_record(feedbacks_provided=1)
    response.flash = "recorded comment"


def record_vote(vote_feedback, tulip):
    int_vote = int(vote_feedback)
    if int_vote <= 1 and int_vote >= (-1) and tulip.target != "0":
        tulip.set_vote(int_vote)
        response.flash = ("Thanks for your contribution: actual Tulip "
                         "pertinence rate: "), tulip.get_pertinentness()
    else:
        response.flash = ("Invalid vote provided thru HTTP header "
                          "manipulation: do you wanna work with us?")


def status():
    """
    The main TULIP status page
    """
    try:
        tulip_url = request.args[0]
    except IndexError:
        return dict(err=True)

    try:
        tulip = Tulip(url=tulip_url)
    except:
        return dict(err=True)

    leak = tulip.get_leak()
    target = gl.get_target(tulip.target)

    if tulip.target == "0":
        whistleblower = True
        target_url = ''
    else:
        whistleblower = False
        target_url = "target/" + tulip.url

    if whistleblower == False:
        # the stats of the whistleblower don't stay in him own tulip
        # (also ifi its unique!)
        if leak.spooled:
            download_available = int(tulip.downloads_counter) < \
                                 int(tulip.allowed_downloads)
        else:
            download_available = -1
        access_available = access_increment(tulip)
        counter_accesses = tulip.accesses_counter
        limit_counter = tulip.allowed_accesses
    else:
        # the stats of the whistleblower stay in the leak/material
        # entry (is it right ?)
        download_available = False
        if leak.whistleblower_access:
            new_count = int(leak.whistleblowing_access) + 1
            leak.whistleblower_access = new_count
        else:
            leak.whistleblower_counter = 1

        counter_accesses = leak.whistleblower_access
        limit_counter = int("50")  # settings.max_submitter_accesses
        access_available = True

    # check if the comment or a vote has been provided:
    if request.vars and request.vars.Comment:
        record_comment(request.vars.Comment, tulip)

    if request.vars and request.vars.Vote:
        record_vote(request.vars.Vote, tulip)

    # configuration issue
    # *) if we want permit, in Tulip, to see how many download/clicks has
    #    been doing from the receiver, we need to pass the entire tulip
    #    list, because in fact the information about "counter_access"
    #    "downloaded_access" are different for each tulip.
    # or if we want not permit this information crossing, the interface simply
    # has to stop in printing other receiver behaviour.
    # now is implement the extended version, but need to be selectable by the
    # maintainer.
    tulipUsage = []
    flowers = db(db.tulip.leak_id == leak.get_id()).select()
    for singleTulip in flowers:
        if singleTulip.leak_id == tulip.get_id():
            tulipUsage.append(singleTulip)
        else:
            tulipUsage.append(singleTulip)
    # this else is obviously an unsolved bug, but at the moment 0 lines seem
    # to match in leak_id

    feedbacks = []
    usersComment = db(db.comment.leak_id == leak.get_id()).select()
    for singleComment in usersComment:
        if singleComment.leak_id == leak.get_id():
            feedbacks.append(singleComment)

    return dict(err=None,
            access_available=access_available,
            download_available=download_available,
            whistleblower=whistleblower,
            tulip_url=tulip_url,
            leak_id=leak.id,
            leak_title=leak.title,
            leak_tags=leak.tags,
            leak_desc=leak.desc,
            leak_extra=leak.get_extra(),
            leak_material=leak.material,
            tulip_accesses=counter_accesses,
            tulip_allowed_accesses=limit_counter,
            tulip_download=tulip.downloads_counter,
            tulip_allowed_download=tulip.allowed_downloads,
            tulipUsage=tulipUsage,
            feedbacks=feedbacks,
            feedbacks_n=tulip.get_feedbacks_provided(),
            pertinentness=tulip.get_pertinentness(),
            previous_vote=tulip.get_vote(),
            name=tulip.target,
            target_url=target_url,
            targets=gl.get_targets("ANY"),
            files=pickle.loads(leak.material.file))


def download_increment(t):

    if (int(t.downloads_counter) > int(t.allowed_downloads)):
        return False

    if t.downloads_counter:
        new_count = int(t.downloads_counter) + 1
        db.tulip[t.target].update_record(downloads_counter=new_count)
    else:
        db.tulip[t.target].update_record(downloads_counter=1)

    return True


def download():
    import os

    try:
        tulip_url = request.args[0]
    except IndexError:
        return dict(err=True)

    try:
        t = Tulip(url=tulip_url)
    except:
        redirect("/tulip/" + tulip_url)

    target = gl.get_target(t.target)

    if not download_increment(t):
        redirect("/tulip/" + tulip_url)

    leak = t.get_leak()

    response.headers['Content-Type'] = "application/octet"
    response.headers['Content-Disposition'] = 'attachment; filename="' + \
                                              tulip_url + '.zip"'

    download_file = os.path.join(request.folder, 'material/',
                           db(db.submission.leak_id==leak.id).select().first(
                           ).dirname + '.zip')

    # XXX to make proper handlers to manage the fetch of dirname
    return response.stream(open(download_file, 'rb'))


def forward():
    """
    Controller for the page that lets the target to forward the tulip to
    another group.
    """
    try:
        tulip_url = request.args[0]
    except IndexError:
        return dict(err=True, targetgroups=[])

    try:
        tulip = Tulip(url=tulip_url)
    except:
        return dict(err=True, targetgroups=[])

    notified_groups = tulip.get_leak().get_notified_targetgroups()
    all_groups = gl.get_targetgroups()
    groups = {}
    for group in all_groups:
        if not group in notified_groups:
            groups[group] = all_groups[group]
    # Trying to get group ids from POST
    try:
        print request.post_vars["group"]
        group_ids = [int(x) for x in request.post_vars["group"]]
        print group_ids
    except (KeyError, ValueError):
        # if there's no post data get all targets for the view
        # the view will create a form to submit the group to
        # send material to
        return dict(err=False, targetgroups=groups,
                    notified_groups=notified_groups)
    else:
        for group_id in group_ids:
            tulip.get_leak().notify_targetgroup(group_id)
        redirect("/")
        # XXX What to do when done?
        #return dict(err=False, targetgroups=groups,
        #            notified_groups=notified_groups)
