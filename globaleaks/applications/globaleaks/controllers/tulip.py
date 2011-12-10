#coding: utf-8
"""
This controller module contains every controller for accessing the tulip
from a target
"""

import gluon.contrib.simplejson as json
import os
import shutil

mutils = local_import('material').utils()

@configuration_required
def index():
    import hashlib

    form = SQLFORM.factory(Field('Receipt', requires=IS_NOT_EMPTY()))
    if form.accepts(request.vars, session):
        req = request.vars

        leak_number = req.Receipt.replace(' ', '')
        tulip_url = hashlib.sha256(leak_number).hexdigest()
        redirect("/globaleaks/tulip/status/" + tulip_url)

    redirect("/")

def access_increment(tulip):
    if tulip.accesses_counter:
        new_count = int(tulip.accesses_counter) + 1
        db.tulip[tulip.id].update_record(accesses_counter=str(new_count))
    else:
        db.tulip[tulip.id].update_record(accesses_counter="1")

    db.commit()

    if int(tulip.allowed_accesses) != 0 and \
       int(tulip.accesses_counter) > int(tulip.allowed_accesses):
        return True
    else:
        return False


# http://games.adultswim.com/robot-unicorn-attack-twitchy-online-game.html
def record_comment(comment_feedback, tulip):
    leak_id = tulip.get_leak().get_id()
    db.comment.insert(leak_id=leak_id,
                      commenter_name=tulip.get_target_name(),
                      commenter_id=tulip.get_target(),
                      comment=comment_feedback)
    db.commit()
    for t_id in gl.get_targets(None):
        target = gl.get_target(t_id)
        try:
            tulip_url = db((db.tulip.leak_id==leak_id) & (db.tulip.target_id==t_id.id)).select().first().url
            db.notification.insert(target=target.name,
                    address=target.contact,
                    tulip=tulip_url,
                    leak_id=leak_id,
                    type="comment")
        except:
            pass

    db.commit()

    if tulip.feedbacks_provided:
        new_count = int(tulip.feedbacks_provided) + 1
        db.tulip[tulip.id].update_record(feedbacks_provided=new_count)
    else:
        db.tulip[tulip.id].update_record(feedbacks_provided=1)

FileUpload = UploadHandler()

@configuration_required
@request.restful()
def fileupload():
    """
    Controller for file uploading for leak updating
    """
    response.view = 'generic.json'

    if not session.add_files:
        session.add_files = []

    def GET(tulip_url, file=None, deletefile=None, uploads=None, commit=None):
        try:
            tulip_url = request.args[0]
            tulip = Tulip(url=tulip_url)
        except:
            return json.dumps({"success": "false"})
        if not tulip.is_wb():
            return json.dumps({"success": "false"})

        if deletefile:
            session.add_files = [f for f in session.add_files \
                                 if f.filename != deletefile]
            return json.dumps(FileUpload.delete(uploads=True))
        elif file:
            upload = json.loads(FileUpload.get())

            filedir = FileUpload.get_file_dir(leak_id=tulip.leak.id)

            src_file = os.path.join(request.folder, 'uploads',
                                    session.upload_dir, upload[0]['name'])
            dst_folder = os.path.join(request.folder, 'material', filedir)

            return json.dumps(upload)
        elif commit:
            print "Session value: %s" % session.add_files
            if not session.add_files:
                return json.dumps({"success": "false"})
            filedir = FileUpload.get_file_dir(leak_id=tulip.leak.id)
            # finding right progressive number
            prog = 1
            dst_folder = os.path.join(request.folder, 'material',
                                      filedir, str(prog))
            while os.path.exists(dst_folder):
                prog += 1
                dst_folder = os.path.join(request.folder, 'material',
                                          filedir, str(prog))
            os.makedirs(dst_folder)

            for filedata in session.add_files:
                if os.path.exists(os.path.join(request.folder,
                                               'uploads', session.upload_dir,
                                               filedata.filename)):
                    src_file = os.path.join(request.folder, 'uploads',
                                            session.upload_dir, filedata.filename)
                    try:
                        shutil.move(src_file,
                                    os.path.join(dst_folder.decode("utf-8"),
                                                 filedata.filename))
                    except OSError:
                        pass
                else:
                    session.add_files.remove(filedata)

            tulip.leak.add_material(tulip.leak.id, prog, None,
                                    file=json.dumps(session.add_files))
            add_files = [(f.ext, f.filename, f.size)
                         for f in session.add_files]
            session.add_files = None
            # Leak needs to be spooled again
            db(db.leak.id == tulip.leak.id).update(spooled=False)

            for t_id in gl.get_targets(None):
                target = gl.get_target(t_id)
                try:
                    t_url = db((db.tulip.leak_id==leak_id) & (db.tulip.target_id==t_id.id)).select().first().url
                    db.notification.insert(target=target.name,
                            address=target.contact,
                            tulip=t_url,
                            leak_id=tulip.leak.id,
                            type="material")
                except:
                    pass

            db.commit()

            return json.dumps({"success": "true", "data": add_files})
        elif uploads:
            return "not implemented"
        else:
            return json.dumps({"success": "false"})

    def POST(tulip_url, **vars):
        try:
            tulip = Tulip(url=tulip_url)
        except:
            return json.dumps({"success": "false"})
        if not tulip.is_wb():
            return json.dumps({"success": "false"})
        upload = FileUpload.post(tulip.leak.id)

        upload = json.loads(upload)

        filedata = Storage()

        # Store the number of bytes of the uploaded file
        filedata.bytes = upload[0]['size']

        # Store the file size in human readable format
        filedata.size = mutils.human_size(filedata.bytes)

        filedata.fileid = upload[0]['id']

        # Store filename and extension
        filedata.filename = upload[0]['name']

        filedata.ext = mutils.file_type(upload[0]['name'].split(".")[-1])

        session.add_files.append(filedata)

        return json.dumps(upload)

    return locals()

@configuration_required
#@auth.requires(((request and request.args and request.args[0]) and
#                (Tulip(url=request.args[0]).target == "0" or not
#                 (gl.get_target_hash(int(Tulip(url=request.args[0]).get_target())))
#                )) or auth.has_membership('targets'))
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
        return dict(err=True, delete=None)

    leak = tulip.get_leak()

    # those are the error not handled by the try/except before
    if tulip.id == -1:
        return dict(err=True, delete=None)

    whistleblower_msg_html = ''
    if tulip.target == "0":
        whistleblower = True
        session.target = None
        with open(settings.globals.whistleblower_file) as filestream:
            whistleblower_msg_html = filestream.read()

        target_url = ''
        delete_capability = False
    else:
        session.admin = False
        session.target = tulip_url
        whistleblower = False
        target_url = "target/" + tulip.url
        try:
            delete_capability = (gl.get_target(int(tulip.get_target()))).delete_cap
        except:
            delete_capability = None

    # check if the tulip has been requested to be deleted
    if request.vars and request.vars.delete and delete_capability:
        deleted_tulips = tulip.delete_bros()
        return dict(err=False, delete=deleted_tulips)

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

    # configuration issue
    # *) if we want permit, in Tulip, to see how many download/clicks has
    #    been doing from the receiver, we need to pass the entire tulip
    #    list, because in fact the information about "counter_access"
    #    "downloaded_access" are different for each tulip.
    # or if we want not permit this information crossing, the interface simply
    # has to stop in printing other receiver behaviour.
    # now is implement the extended version, but need to be selectable by the
    # maintainer.
    tulip_usage = []
    flowers = db(db.tulip.leak_id == leak.get_id()).select()
    for single_tulip in flowers:
        targetname = db(db.target.id == single_tulip.target_id).select(db.target.name).first()
        if targetname:
            if tulip.target == single_tulip.target_id:
                targetname = "You"
            else:
                targetname = targetname.name

        if single_tulip.leak_id == tulip.get_id():
            tulip_usage.append((targetname,single_tulip))
        else:
            tulip_usage.append((targetname, single_tulip))
    # this else is obviously an unsolved bug, but at the moment 0 lines seem
    # to match in leak_id

    feedbacks = []
    users_comment = db(db.comment.leak_id == leak.get_id()).select()
    for single_comment in users_comment:
        if single_comment.leak_id == leak.get_id():
            feedbacks.append(single_comment)

    jQueryHelper = local_import('jquery_helper')
    upload_template = jQueryHelper.upload_tmpl()
    download_template = jQueryHelper.download_tmpl()
    submission_mats = [(m.url, json.loads(m.file)) for m in leak.material]
    return dict(err=None,delete=None,
            access_available=access_available,
            download_available=download_available,
            whistleblower=whistleblower,
            whistleblower_msg_html=whistleblower_msg_html,
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
            tulipUsage=tulip_usage,
            feedbacks=feedbacks,
            feedbacks_n=tulip.get_feedbacks_provided(),
            receiver_id=tulip.target,
            target_del_cap=delete_capability,
            target_url=target_url,
            targets=gl.get_targets("ANY"),
            submission_materials=submission_mats,
            jQuery_templates=(XML(upload_template),
                              XML(download_template))
            )


def download_increment(tulip):

    if (int(tulip.downloads_counter) > int(tulip.allowed_downloads)):
        return False

    if tulip.downloads_counter:
        new_count = int(tulip.downloads_counter) + 1
        db.tulip[tulip.target].update_record(downloads_counter=new_count)
    else:
        db.tulip[tulip.target].update_record(downloads_counter=1)

    return True


@configuration_required
def download():
    import os

    try:
        tulip_url = request.args[0]
    except IndexError:
        return dict(err=True)

    try:
        t = Tulip(url=tulip_url)
    except:
        redirect("/globaleaks/tulip/status/" + tulip_url)

    if not download_increment(t):
        redirect("/globaleaks/tulip/status/" + tulip_url)

    leak = t.get_leak()

    filename = db(db.submission.leak_id==leak.id).select().first().dirname
    try:
        filename = "%s-%s" % (filename, request.args[1])
    except IndexError:
        pass
    response.headers['Content-Type'] = "application/octet"
    response.headers['Content-Disposition'] = 'attachment; filename="' + \
                                              filename + '.zip"'

    download_file = os.path.join(request.folder, 'material/',
                                 filename + '.zip')

    # XXX to make proper handlers to manage the fetch of dirname
    return response.stream(open(download_file, 'rb'))
