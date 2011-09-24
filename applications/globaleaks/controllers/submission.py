import os

def index():
    leaker_number = None

    """form_content = (Field('Title', requires=IS_NOT_EMPTY()),
                    Field('Description', 'text', requires=IS_NOT_EMPTY()),
                    Field('material1', 'upload', uploadfolder=os.path.join(request.folder,'uploads/')),
                    Field('material2', 'upload', uploadfolder=os.path.join(request.folder,'uploads/')),
                    Field('material3', 'upload', uploadfolder=os.path.join(request.folder,'uploads/')),
                    Field('metadata', 'boolean', requires=NOT_IMPLEMENTED("tulip-metadata-sanitization")),
                    Field('disclaimer', 'boolean', requires=IS_EQUAL_TO("on", error_message="Please read the disclaimer"))
                    )
    """
    # form = SQLFORM.factory(*form_content)
    # temporary comment: syntax error !?
    # form = SQLFORM.factory(*form_content,labels = {'disclaimer':'Accept and have read the disclaimer', 'metadata':'Metadata sanitization'})

    leaker_number = randomizer.generate_tulip_receipt()

    if not session.wb_id:
        session.wb_id = randomizer.generate_wb_id()

    form = FORM(TABLE(
            TR('Title', INPUT(_name='Title', requires=IS_NOT_EMPTY())),
            TR('Description:',TEXTAREA(_name='Description',
                                       requires=IS_NOT_EMPTY())),
            TR('Material',DIV(_id='file-uploader'), _id='file-uploader-js'),
            TR('Material:', INPUT(_name='material', _type='file'),
                                  _id='file-uploader-nonjs'),
            TR('Metadata:',INPUT(_name='metadata', _type='checkbox',
                                 _class="notimplemented")),
            TR('Accept Disclaimer:',
               INPUT(_name='disclaimer',
                     _type='checkbox',
                     requires=IS_EQUAL_TO("on",
                              error_message="Please accept the disclaimer"))),
            TR('', INPUT(_name='submit', _type='submit'))))

    response.flash = "You are the Whistleblower"

    if form.accepts(request.vars, session):
        l = request.vars

        leak_id = gl.create_leak(l.Title, l.Description, None, None,
                                 "demo", l.Tags, number=leaker_number[1])

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
                    filename = request.vars.material.filename
                    tmp_file = db.material.file.store(request.body, filename)

                    dst_folder = os.path.join(request.folder, 'material/' + \
                                              str(leak_id.id) + '/')
                    if not os.path.isdir(dst_folder):
                        os.mkdir(dst_folder)
                    os.rename(os.path.join(request.folder, 'uploads/') + \
                              tmp_file, dst_folder + filename)
                except:
                    pass

        leak = Leak(leak_id)
        leak.add_material(leak_id, "demo", "demo")

        for tulip in leak.tulips:
            target = gl.get_target(tulip.target)

            if tulip.target == "0":
                leaker_tulip = tulip.url
                continue

            if target.status == "subscribed":
                print "adding to mail, subscribed dude"
                db.mail.insert(target=target.name,
                        address=target.url, tulip=tulip.url)
        pretty_number = leaker_number[0][:3] + " " + leaker_number[0][3:6] + \
                        " " + leaker_number[0][6:]

        return dict(leak_id=leak_id, leaker_tulip=pretty_number, form=None)
    elif form.errors:
        response.flash = 'form has errors'

    return dict(form=form, leak_id=None, tulip=None, tulips=None)

def upload():
    # File upload in a slightly smarter way
    # http://www.web2py.com/book/default/chapter/06#Manual-Uploads
    for f in request.vars:
        if f == "qqfile":
            filename = request.vars.qqfile
            tmp_file = db.material.file.store(request.body, filename)

            fldr = db(db.submission.session==session.wb_id
                         ).select().first()
            if not fldr:
                fldr = randomizer.generate_dirname()
                session.dirname = fldr
            else:
                fldr = str(fldr.dirname)
            dst_folder = os.path.join(request.folder, 'material/' + fldr + '/')
            if not os.path.isdir(dst_folder):
                os.makedirs(dst_folder)
            os.rename(os.path.join(request.folder, 'uploads/') +
                      tmp_file, dst_folder + filename)
            return response.json({'success':'true'})

