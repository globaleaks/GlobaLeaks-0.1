import os
def index():
    leaker_number = None
    form_content = (Field('Title', requires=IS_NOT_EMPTY()),
                    Field('Description', 'text', requires=IS_NOT_EMPTY()),
                    Field('material1', 'upload', uploadfolder=os.path.join(request.folder,'uploads/')),
                    Field('material2', 'upload', uploadfolder=os.path.join(request.folder,'uploads/')),
                    Field('material3', 'upload', uploadfolder=os.path.join(request.folder,'uploads/')),
                    Field('dislaimer', 'boolean', requires=IS_EQUAL_TO("on", error_message="Please read the disclaimer")))
   
    form = SQLFORM.factory(*form_content)
    
    response.flash = "You are the Whistleblower"
    
    if form.accepts(request.vars, session):
        l = request.vars
        leaker_number = randomizer.generate_tulip_receipt()
        
        leak_id = gl.create_leak(l.Title, l.Description, None, None,
                "demo", l.Tags, number=leaker_number[1])
                
        if(l.material1 or l.material2 or l.material3):
            db.material.insert(leak_id=leak_id,
                    url="demo", type="demo")
            
        
        i = 0
        
        #XXX Refactor me please
        for f in os.listdir(os.path.join(request.folder,'uploads/')):
            ext = f.split(".")[-1:][0]
            dst_folder = os.path.join(request.folder, 'material/' + str(leak_id.id) + '/')
            if not os.path.isdir(dst_folder):
                os.mkdir(dst_folder)
            os.rename(os.path.join(request.folder, 'uploads/') + f, dst_folder + str(i) + "." + ext)
            i += 1
        #response.flash = 'form accepted'
        leak = Leak(leak_id)
                                
        for tulip in leak.tulips:
            target = gl.get_target(tulip.target)
            
            if tulip.target=="0":
                leaker_tulip = tulip.url
                continue

            print "%s: %s" % (tulip.target, target)
           
            if target.status == "subscribed":
                db.mail.insert(target=target.name,
                        address=target.uri, tulip=tulip.url)
                            
            
        return dict(leak_id=leak_id, leaker_tulip=leaker_number[0], form=None)
    elif form.errors:
        response.flash = 'form has errors'
    
    return dict(form=form, leak_id=None, tulip=None, tulips=None)
