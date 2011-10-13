import os,random
import pickle
import time
from gluon.tools import Service
import gluon.contrib.simplejson as json

mutils = local_import('material').utils()

@service.json
def info():
    output = [{'label' : 'Description',
            'type': 'text', 'name' : 'desc',
            'desc': 'Describe your issue'},
            {'label' : 'Title',
            'type': 'string', 'name': 'title',
            'desc': 'Give a title to your submission'}]
    output.append(settings.extrafields.fields)
    return output

@service.json
def post():
    wb_number = randomizer.generate_tulip_receipt()

    data = json.loads(request.vars.fields)
    data['spooled'] = False
    data['submission_timestamp'] = time.time()

    leak_id = db.leak.insert(**data)

    gl.create_leak(leak_id, "ALL", wb_number[1])

    # If a session has not been created yet, create one.
    if not session.wb_id:
        session.wb_id = randomizer.generate_wb_id()

    if not db(db.submission.session==session.wb_id).select():
        db.submission.insert(session=session.wb_id,
                             leak_id=leak_id,
                             dirname=session.dirname)
    if not session.files:
        session.files = []
    pfile = pickle.dumps(session.files)

    leak = Leak(leak_id)
    leak.add_material(leak_id, None, None, file=pfile)

    for tulip in leak.tulips:
        target = gl.get_target(tulip.target)

        if tulip.target == "0":
            leaker_tulip = tulip.url
            continue

        if target.status == "subscribed":
            db.mail.insert(target=target.name,
                    address=target.url, tulip=tulip.url)
    pretty_number = wb_number[0][:3] + " " + wb_number[0][3:6] + \
                    " " + wb_number[0][6:]
    session.dirname = None
    session.wb_id = None
    session.files = None

    return json.dumps(dict(leak_id=leak_id, leaker_tulip=pretty_number,
                form=None, tulip_url=tulip.url))

def call():
    return service()


def index():
    """
    This is the main submission page.
    """
    # Generate the number the WB will use to come back to
    # his submission
    wb_number = randomizer.generate_tulip_receipt()

    # If a session has not been created yet, create one.
    if not session.wb_id:
        session.wb_id = randomizer.generate_wb_id()

    # Generate the material upload elements
    # JavaScript version
    material_js = TR('Material',DIV(_id='file-uploader'), _id='file-uploader-js')
    # .. and non JavaScript
    material_njs = TR('Material:', INPUT(_name='material', _type='file'),\
                                  _id='file-uploader-nonjs')

    # Use the web2py captcha setting to generate a Captcha
    captcha = TR('Are you human?',auth.settings.captcha)

    disclaimer_text = TR('Accept Disclaimer',settings.globals.disclaimer)
    disclaimer = TR("",INPUT(_name='agree',value=True,_type='checkbox'))

    # The default fields and labels
    form_fields = ['title', 'desc']
    form_labels={'title': 'Title', 'desc': 'Description'}

    # Add to the fields to be displayed the ones inside of
    # the extrafields setting
    for i in settings.extrafields.fields:
        form_fields.append(str(i['name']))
        form_labels[str(i['name'])] = str(i['desc'])

    # Create the actual form
    form = SQLFORM(db.leak,
            fields=form_fields,
            labels=form_labels)

    # Add the extra settings that are not included in the DB
    form[0].insert(-1, material_njs)
    form[0].insert(-1, material_js)
    
    # Check to see if some files have been loaded from a previous session
    if session.files:
        filesul = UL(_id="stored_files")
        # XXX Is this being sanitized?
        for file in session.files:
            filesul.append(LI(SPAN(str(file.filename)),A("delete", \
                                                _href="", _class="stored_file_delete", \
                                                _id=file.fileid)))
            
        form[0].insert(-1, TR('Stored files', filesul))
        
    form[0].insert(-1, captcha)
    form[0].insert(-1, disclaimer_text)
    form[0].insert(-1, disclaimer)

    # Make the submission not spooled and set the timestamp
    form.vars.spooled = False
    form.vars.submission_timestamp=time.time()

    # Insert all the data into the db
    if form.accepts(request.vars, session):

        # XXX Refactor this into something that makes sense
        #
        # Create the leak with the GlobaLeaks factory
        # (the data has actually already been added to db leak,
        #  this just creates the tulips)
        leak_id = gl.create_leak(form.vars.id, "ALL", wb_number[1])

        logger.debug("Submission %s", request.vars)

        # XXX probably a better way to do this
        # Create a record in submission db associated with leak_id
        # used to keep track of sessions
        if not db(db.submission.session==session.wb_id).select():
            db.submission.insert(session=session.wb_id,
                                 leak_id=leak_id,
                                 dirname=session.dirname)

        # XXX Since files are processed via AJAX, maybe this is unecessary?
        #     if we want to keep it to allow legacy file upload, then the
        #     file count should only be one.
        # File upload in a slightly smarter way
        # http://www.web2py.com/book/default/chapter/06#Manual-Uploads
        for file in request.vars:
            if file=="material":
                try:
                    f = Storage()
                    f.filename = request.vars.material.filename
                    tmp_file = db.material.file.store(request.body, filename)

                    f.ext = mutils.file_type(filename.split(".")[-1])

                    tmp_fpath = os.path(os.path.join(request.folder, 'uploads/') + \
                                    tmp_file + filename)

                    f.size = os.path.getsize(tmp_fpath)
                    files.append(f)

                    dst_folder = os.path.join(request.folder, 'material/' + \
                                              str(leak_id.id) + '/')
                    if not os.path.isdir(dst_folder):
                        os.mkdir(dst_folder)
                    os.rename(os.path.join(request.folder, 'uploads/') + \
                              tmp_file, dst_folder + filename)
                except:
                    logger.error("There was an error in processing the submission files.")
                    pass

        # The metadata associated with the file is stored inside the session variable
        # this should be safe to use this way.
        if not session.files:
            session.files = []
        # XXX verify that this is safe
        pfile = pickle.dumps(session.files)

        # Instantiate the Leak object
        leak = Leak(leak_id)
        # Create the material entry for the submitted data
        leak.add_material(leak_id, None, "localfs", file=pfile)

        # Go trough all of the previously generated TULIPs
        for tulip in leak.tulips:
            target = gl.get_target(tulip.target)
            
            # Ignore WB tulips
            if tulip.target == "0":
                continue

            if target.status == "subscribed":
                # add subscribed targets to the mail db
                # when the cron job passes they will recieve a mail
                db.mail.insert(target=target.name,
                        address=target.url, tulip=tulip.url)
                
        # Make the WB number be *** *** *****
        pretty_number = wb_number[0][:3] + " " + wb_number[0][3:6] + \
                        " " + wb_number[0][6:]
                        
        # Clean up all sessions
        session.dirname = None
        session.wb_id = None
        session.files = None

        return dict(leak_id=leak_id, leaker_tulip=pretty_number,
                    form=None, tulip_url=tulip.url)

    elif form.errors:
        response.flash = 'form has errors'

    return dict(form=form, leak_id=None, tulip=None, tulips=None)

@service.json
def upload():
    """
    Used for storing the uploaded files. To be invoked
    only from AJAX or as a web service.
    """
    
    # File upload in a slightly smarter way
    # http://www.web2py.com/book/default/chapter/06#Manual-Uploads
    if not session.files:
        session.files = []
        
    for f in request.vars:
        # Process the qqfile POST vars
        if f == "qqfile":
            filename = request.vars.qqfile
            
            # Store the file to a temporary location and get the path
            tmp_file = db.material.file.store(request.body, filename)
            
            # Store filename and extention            
            filedata = Storage()
            filedata.filename = filename
            filedata.ext = mutils.file_type(filename.split(".")[-1])

            tmp_fpath = os.path.join(request.folder, 'uploads/') + \
                                tmp_file
            
            # Store the file size in human readable format
            filedata.size = mutils.human_size(os.path.getsize(tmp_fpath))

            # Generate a random file ID
            # XXX is this a good way of doing it?
            filedata.fileid = random.randint(0,1000000000000000)

            # Store all the data reated to the file to a sessions variable
            session.files.append(filedata)

            
            filedir = db(db.submission.session==\
                      session.wb_id).select().first()
            
            if not filedir:
                if not session.dirname:
                    filedir = randomizer.generate_dirname()
                    session.dirname = filedir
                else:
                    filedir = session.dirname
            else:
                filedir = str(filedir.dirname)
            dst_folder = os.path.join(request.folder, 'material/' + filedir + '/')
            
            if not os.path.isdir(dst_folder):
                os.makedirs(dst_folder)
            os.rename(os.path.join(request.folder, 'uploads/') +
                      tmp_file, dst_folder + filename)

            # this TODO XXX db.material.async_id need to be updated with filedata.fileid
            # and used as research key in sendinfo, to add details and title
            # XXX XXX XXX XXX

            return response.json({'success':'true', 'fileid': filedata.fileid})

        if f == "delete":
            for file in session.files:
                files = []
                if str(file.fileid) == str(request.vars.delete):
                    dst_folder = os.path.join(request.folder, 'material/' + session.dirname + '/')
                    try:
                        os.remove(dst_folder + file.filename)
                    except:
                        logger.error("File requested for deletion is already deleted.")
                else:
                    files.append(file)
                session.files = files
                return response.json({'success':'true'})


def sendinfo():
    logger = local_import('logger').start_logger(settings.logging)

    if not session.files:
        session.files = []

    for f in request.vars:
        logger.info("field : %s", f)
        if f == "info_id":
            indexed_file_id = request.vars.info_id
            logger.info("info-id: %s", indexed_file_id)
    # odd ? /tmp/globaleaks.log return a very strange output

    return response.json({'success':'true'})

