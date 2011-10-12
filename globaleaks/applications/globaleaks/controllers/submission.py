import os,random
import pickle

mutils = local_import('material').utils()


def index():
    leaker_number = None

    # form = SQLFORM.factory(*form_content)
    # temporary comment: syntax error !?
    # form = SQLFORM.factory(*form_content,labels = {'disclaimer':'Accept and have read the disclaimer', 'metadata':'Metadata sanitization'})

    leaker_number = randomizer.generate_tulip_receipt()

    if not session.wb_id:
        session.wb_id = randomizer.generate_wb_id()

    material_js = TR('Material',DIV(_id='file-uploader'), _id='file-uploader-js')
    material_njs = TR('Material:', INPUT(_name='material', _type='file'),\
                                  _id='file-uploader-nonjs')

    captcha = TR('Are you human?',auth.settings.captcha)

    disclaimer_text = TR('Accept Disclaimer',settings.globals.disclaimer)
    disclaimer = TR("",INPUT(_name='agree',value=True,_type='checkbox'))
    form_fields = ['title', 'desc']
    form_labels={'title': 'Title', 'desc': 'Description'}

    for i in settings.extrafields.fields:
        form_fields.append(str(i['name']))
        form_labels[str(i['name'])] = str(i['desc'])

    form = SQLFORM(db.leak,
            fields=form_fields,
            labels=form_labels)

    form[0].insert(-1, material_njs)
    form[0].insert(-1, material_js)
    form[0].insert(-1, captcha)
    form[0].insert(-1, disclaimer_text)
    form[0].insert(-1, disclaimer)

    if form.accepts(request.vars, session):

        leak_id = gl.create_leak(form.vars.id, "ALL", leaker_number[1]) #l.Title, l.Description, None, None,
                                 #"demo", l.Tags, number=leaker_number[1])
        # adding association submission -> leak_id
        if not db(db.submission.session==session.wb_id).select():
            db.submission.insert(session=session.wb_id,
                                 leak_id=leak_id,
                                 dirname=session.dirname)

        #XXX Refactor me please
        # Create the material directory if it does not exist
        # the name of the directory is the leak id

        """for f in os.listdir(os.path.join(request.folder,'uploads/')):
            ext = f.split(".")[-1:][0]
            dst_fo.folderpath.join(request.folder, 'material/' + str(leak_id.id) + '/')
            if not os.path.isdir(dst_folder):
                os.mkdir(dst_folder)
            os.rename(os.path.join(request.folder, 'uploads/') + f, dst_folder + str(i) + "." + ext)
            i += 1"""

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
                    pass
        # XXX alarm alert, please sanitize this data properly XXX
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
        pretty_number = leaker_number[0][:3] + " " + leaker_number[0][3:6] + \
                        " " + leaker_number[0][6:]
        session.dirname = None
        session.wb_id = None
        session.files = None

        return dict(leak_id=leak_id, leaker_tulip=pretty_number,
                    form=None, tulip_url=tulip.url)
    elif form.errors:
        response.flash = 'form has errors'

    return dict(form=form, leak_id=None, tulip=None, tulips=None)

def upload():
    # File upload in a slightly smarter way
    # http://www.web2py.com/book/default/chapter/06#Manual-Uploads
    if not session.files:
        session.files = []
    for f in request.vars:
        if f == "qqfile":
            filename = request.vars.qqfile
            tmp_file = db.material.file.store(request.body, filename)

            fls = Storage()
            fls.filename = filename

            fls.ext = mutils.file_type(filename.split(".")[-1])

            tmp_fpath = os.path.join(request.folder, 'uploads/') + \
                                tmp_file

            fls.size = mutils.human_size(os.path.getsize(tmp_fpath))

            fls.fileid = random.randint(0,1000000000000000)

            session.files.append(fls)

            fldr = db(db.submission.session==session.wb_id).select().first()
            if not fldr:
                if not session.dirname:
                    fldr = randomizer.generate_dirname()
                    session.dirname = fldr
                else:
                    fldr = session.dirname
            else:
                fldr = str(fldr.dirname)
            dst_folder = os.path.join(request.folder, 'material/' + fldr + '/')
            if not os.path.isdir(dst_folder):
                os.makedirs(dst_folder)
            os.rename(os.path.join(request.folder, 'uploads/') +
                      tmp_file, dst_folder + filename)

            # this TODO XXX db.material.async_id need to be updated with fls.fileid
            # and used as research key in sendinfo, to add details and title
            # XXX XXX XXX XXX

            return response.json({'success':'true', 'fileid': fls.fileid})

        if f == "delete":
            for file in session.files:
                if str(file.fileid) == str(request.vars.delete):
                    dst_folder = os.path.join(request.folder, 'material/' + session.dirname + '/')
                    os.remove(dst_folder + file.filename)
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

