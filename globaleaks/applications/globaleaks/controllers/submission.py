#coding: utf-8
"""
This controller module contains every controller for leak submission.
"""

import os
import random
import time
from gluon.tools import Service
import gluon.contrib.simplejson as json
import shutil
import base64

T.force("EN")
#FormWizard = local_import('plugin_PowerFormWizard')

mutils = local_import('material').utils()
Anonymity = local_import('anonymity')
jQueryHelper = local_import('jquery_helper')
FileHelper = local_import('file_helper')

# This should be merged with the following service
#
@configuration_required
@request.restful()
def api():

    response.view = 'generic.json'

    def GET(*r):
        output = [{'label': 'Description',
                   'type': 'text',
                   'name': 'desc',
                   'desc': 'Describe your issue'},
                {'label': 'Title',
                 'type': 'string',
                 'name': 'title',
                 'desc': 'Give a title to your submission'}]
        output.append(settings.extrafields.fields)
        return dict(result=output)

    def POST(**data):
        wb_number = randomizer.generate_tulip_receipt()
        # XXX verify that it's working
        if not data.has_key("targetgroup"):
            return result.error
        else:
            group_ids = data["targetgroup"]
        # change group names to group ids
        group_ids = [gl.get_group_id(g) for g in group_ids]
        data['spooled'] = False
        data['submission_timestamp'] = time.time()

        result = db.leak.validate_and_insert(**data)

        if result.error:
            return result.error
        else:
            leak_id = result.id

        # If a session has not been created yet, create one.
        if not session.wb_id:
            session.wb_id = randomizer.generate_wb_id()

        if not db(db.submission.session==session.wb_id).select():
            db.submission.insert(session=session.wb_id,
                                 leak_id=leak_id,
                                 dirname=session.dirname)
        if not session.files:
            session.files = []
        pfile = json.dumpsumps(session.files)

        leak = Leak(leak_id)
        leak.add_material(leak_id, None, None, file=pfile)

        # generation of tulips: the first, in GlobaLeaks object, aim to create
        # the whistleblower tulip
        gl.create_tulip(leak_id, 0, wb_number[1])

        # this loop, create the tulip for the receivers
        for group_id in group_ids:
            leak.crate_tulip_by_group(group_id)

        # format the pretty number for being saved like a phone number
        pretty_number = wb_number[0][:3] + " " + wb_number[0][3:6] + \
                        " " + wb_number[0][6:]

        session.dirname = None
        session.wb_id = None
        session.files = None

        return dict(leak_id=leak_id, leaker_tulip=pretty_number,
                    form=None, tulip_url=wb_number[1])

    return locals()

FileUpload = UploadHandler()

# XXX
# This should be made into one web service
# Integrate the methods suggested in the REST interface specification
@configuration_required
@request.restful()
def fileupload():
    response.view = 'generic.json'
    if not session.files:
        session.files = []

    def GET(file=None, deletefile=None, uploads=None):

        if deletefile:
            session.files = [f for f in session.files if f.filename != deletefile]
            return json.dumps(FileUpload.delete())
        elif file:
            upload = json.loads(FileUpload.get())

            filedir = FileUpload.get_file_dir()

            src_file = os.path.join(request.folder, 'uploads',
                                    session.upload_dir, upload[0]['name'])
            dst_folder = os.path.join(request.folder, 'material', filedir)

            return json.dumps(upload)
        elif uploads:
            return "not implemented"

        else:
            return "not implemented"

    def POST(**vars):
        upload = FileUpload.post()

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

        session.files.append(filedata)

        filedir = FileUpload.get_file_dir()

        src_file = os.path.join(request.folder, 'uploads', session.upload_dir,
                                upload[0]['name'])
        dst_folder = os.path.join(request.folder, 'material', filedir)

        if not os.path.isdir(dst_folder):
            os.makedirs(dst_folder)

        # XXX this is necessary only for the resume support
        #if upload[0]['size'] == os.path.getsize(src_file):
            #print "THEY MATCH!!!!!.... %s != %s" % (upload[0]['size'], os.path.getsize(src_file))
        os.rename(src_file, os.path.join(dst_folder, upload[0]['name']))

        return json.dumps(upload)

    return locals()

@configuration_required
def index():
    """
    This is the main submission page.
    """
    # Generate the number the WB will use to come back to
    # his submission
    wb_number = randomizer.generate_tulip_receipt()

    # Perform a check to see if the client is using Tor
    anonymity = Anonymity.TorAccessCheck(request.client, request.env)

    # If a session has not been created yet, create one.
    if not session.wb_id:
        session.wb_id = randomizer.generate_wb_id()

    # -- follow a comment preserved since 'the age of the upload'
    #
    # Tor Browser Bundle has JS enabled by default!
    # Hurray! I love you all!!
    # Yeah, even *you* the anti-JS taliban hater!
    # As someone put it, if you think JS is evil remember
    # that the world is in technicolor and not in black and white.
    # Look up, the sun is shining, thanks to jQuery.

    # This is necessary because otherwise web2py will go crazy when
    # it sees {{ }}
    upload_template = jQueryHelper.upload_tmpl()

    download_template = jQueryHelper.download_tmpl()

    # Generate the material upload elements
    # JavaScript version
    material_js = TR('Material',
                     DIV(_id='file-uploader'),
                     _id='file-uploader-js')

    # .. and non JavaScript
    material_njs = DIV(DIV(LABEL("Material:"),
                                _class="w2p_fl"),
                            DIV(INPUT(_name='material', _type='file',
                                      _id='file-uploader-nonjs'),
                                _class="w2p_fc"),
                                _id="file-uploader-nonjs")

    # Use the web2py captcha setting to generate a Captcha
    # captcha = TR('Are you human?', auth.settings.captcha)

    # The default fields and labels
    form_fields = ['title', 'desc']
    form_labels = {'title': 'Title', 'desc': 'Description'}

    form_extras = []

    # Add to the fields to be displayed the ones inside of
    # the extrafields setting
#    for i in settings.extrafields.fields:
#        form_extras.append(str(i['name']))
#        form_fields.append(str(i['name']))
#        form_labels[str(i['name'])] = i['desc']

    if settings.extrafields.wizard:
        the_steps = settings.extrafields.gen_wizard()

        form = FormShaman(db.leak, steps=the_steps)
        # this is the only error handled at the moment, the fact that __init__
        # could return only None, maybe an issue when more errors might be managed
        if not hasattr(form, 'vars'):
            return dict(error='No receiver present in the default group', existing_files=[])

    else:
        form = SQLFORM(db.leak,
                       fields=form_fields,
                       labels=form_labels)

    # Check to see if some files have been loaded from a previous session
    existing_files = []
    if session.files:
        for f in session.files:
            existing_files.append(f)

    # Make the submission not spooled and set the timestamp
    form.vars.spooled = False
    form.vars.submission_timestamp = time.time()

    # Insert all the data into the db
    if form.accepts(request.vars):
        logger.debug("Submission %s", request.vars)

        group_ids = []  # Will contain all the groups selected by the WB

        # XXX Since files are processed via AJAX, maybe this is unecessary?
        #     if we want to keep it to allow legacy file upload, then the
        #     file count should only be one.
        # File upload in a slightly smarter way
        # http://www.web2py.com/book/default/chapter/06#Manual-Uploads
        for var in request.vars:
            if var == "material":
                try:
                    f = Storage()
                    f.filename = request.vars.material.filename

                    tmp_file = db.material.file.store(request.body, filename)
                    logger.info("the tmp_file is [%s] with filename [%s]",
                                tmp_file, filename)

                    f.ext = mutils.file_type(filename.split(".")[-1])

                    tmp_fpath = os.path(os.path.join(request.folder,
                                                     'uploads',
                                                     session.upload_dir,
                                                     tmp_file + filename))

                    f.size = os.path.getsize(tmp_fpath)
                    files.append(f)

                    dst_folder = os.path.join(request.folder,
                                              'material',
                                              str(leak_id.id))
                    if not os.path.isdir(dst_folder):
                        os.mkdir(dst_folder)
                    os.rename(os.path.join(request.folder,
                                           'uploads',
                                           session.upload_dir,
                                           tmp_file),
                              dst_folder + filename)
                # XXX define exception for this except
                except:
                    logger.error("There was an error in processing the "
                                 "submission files.")

            if var.startswith("target_") and var.split("_")[-1].isdigit():
                group_ids.append(var.split("_")[-1])

        # The metadata associated with the file is stored inside
        # the session variable this should be safe to use this way.
        if not session.files:
            session.files = []
        # XXX verify that this is safe
        pfile = json.dumps(session.files)

        # leak_id has been used in the previous code as this value,
        # I'm keeping to don't change the following lines
        leak_id = form.vars.id

        # XXX probably a better way to do this
        # Create a record in submission db associated with leak_id
        # used to keep track of sessions
        if not db(db.submission.session==session.wb_id).select():
            db.submission.insert(session=session.wb_id,
                                 leak_id=leak_id,
                                 dirname=session.dirname)

        # Instantiate the Leak object
        leak = Leak(leak_id)
        # Create the material entry for the submitted data
        leak.add_material(leak_id, None, "localfs", file=pfile)

        # Create the leak with the GlobaLeaks factory
        # (the data has actually already been added to db leak,
        # this just creates the tulips), the first is the whistleblower tulip
        gl.create_tulip(form.vars.id, 0, wb_number[1])

        # create the tulips for every receiver inside a basket

        # if len(group_ids):
        # fixme: we're not considering the selecred group, but *all*
        group_id = db().select(db.targetgroup.ALL).first().id
        leak.create_tulip_by_group(group_id)

        # Make the WB number be *** *** *****
        pretty_number = wb_number[0][:3] + " " + wb_number[0][3:6] + \
                        " " + wb_number[0][6:]

        session.wb_number = pretty_number
        # Clean up all sessions
        session.dirname = None
        session.wb_id = None
        session.files = None

        return dict(leak_id=leak_id, leaker_tulip=pretty_number, error=None,
                    form=None, tulip_url=wb_number[1], jQuery_templates=None,
                    existing_files=existing_files)

    elif form.errors:
        response.flash = 'form has errors'

    return dict(form=form,
                error=None,
                leak_id=None,
                tulip=None,
                tulips=None,
                anonymity=anonymity.result,
                jQuery_templates=(XML(upload_template),
                                  XML(download_template)),
                existing_files=existing_files)
