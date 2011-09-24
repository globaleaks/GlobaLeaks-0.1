import os
from pprint import pprint

def register_whistleblower(leak_id):
    submitter = db.target.insert(id=leak_id)
#    OK, this is putting the user in the target table
#    NEW BUG DETECTED: at the moment the target list is not inside target but 
#    in "mail". now this could be committed because someother will implement the
#    groups management
    if not submitter:
        return
        
    db.target[leak_id].update_record(status="submitter")

def index():
    leaker_number = None
    form_content = (Field('Title', requires=IS_NOT_EMPTY()),
                    Field('Description', 'text', requires=IS_NOT_EMPTY()),
                    Field('material1', 'upload', uploadfolder=os.path.join(request.folder,'uploads/')),
                    Field('material2', 'upload', uploadfolder=os.path.join(request.folder,'uploads/')),
                    Field('material3', 'upload', uploadfolder=os.path.join(request.folder,'uploads/')),
                    Field('metadata', 'boolean', requires=NOT_IMPLEMENTED("tulip-metadata-sanitization")),
                    Field('disclaimer', 'boolean', requires=IS_EQUAL_TO("on", error_message="Please read the disclaimer")),
                    )
         
    form = SQLFORM.factory(*form_content)
    # temporary comment: syntax error !?
    # form = SQLFORM.factory(*form_content,labels = {'disclaimer':'Accept and have read the disclaimer', 'metadata':'Metadata sanitization'})
    
    form = FORM(TABLE(
            TR('Title', INPUT(_name='Title', requires=IS_NOT_EMPTY())),
            TR('Description:',TEXTAREA(_name='Description', requires=IS_NOT_EMPTY())),
            TR('Material:', INPUT(_name='material1', _type='file', _class="disabled")),
            TR('Metadata:',INPUT(_name='metadata', _type='checkbox', _class="notimplemented")),
            TR('Accept Disclaimer:',
                INPUT(_name='disclaimer', _type='checkbox', 
                    requires=IS_EQUAL_TO("on", error_message="Please accept the disclaimer"))),
            TR('', INPUT(_name='submit', _type='submit'))))
    
    response.flash = "You are the Whistleblower"
    
    if form.accepts(request.vars, session):
        l = request.vars
        leaker_number = randomizer.generate_tulip_receipt()
        
        leak_id = gl.create_leak(l.Title, l.Description, None, None,
                "demo", l.Tags, number=leaker_number[1])

        i = 0
        
        #FIXME Refactor me please
        for f in os.listdir(os.path.join(request.folder,'uploads/')):
            ext = f.split(".")[-1:][0]
            dst_folder = os.path.join(request.folder, 'material/' + str(leak_id.id) + '/')
            if not os.path.isdir(dst_folder):
                os.mkdir(dst_folder)
            os.rename(os.path.join(request.folder, 'uploads/') + f, dst_folder + str(i) + "." + ext)
            i += 1
        leak = Leak(leak_id)

        if(i>0):
            leak.add_material(leak_id, "demo", "demo")
        
        # adding the whilstleblower in the target list is required because in tulip.py
        # is checked the counter of access (could expired also for the submitter)
        register_whistleblower(leak_id)
        
        for tulip in leak.tulips:
            target = gl.get_target(tulip.target)
            
            if tulip.target=="0":
                leaker_tulip = tulip.url
                continue

            if target.status == "subscribed":
                print "adding to mail, subscribed dude"
                db.mail.insert(target=target.name,
                        address=target.url, tulip=tulip.url)
        pretty_number = leaker_number[0][:3]+" "+leaker_number[0][3:6]+" " +leaker_number[0][6:]

        return dict(leak_id=leak_id, leaker_tulip=pretty_number, form=None)
    elif form.errors:
        response.flash = 'form has errors'
    
    return dict(form=form, leak_id=None, tulip=None, tulips=None)
