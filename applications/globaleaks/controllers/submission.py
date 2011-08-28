def index():
    form_content = (Field('Title', requires=IS_NOT_EMPTY()),
                    Field('Description', 'text', requires=IS_NOT_EMPTY()),
                    Field('Tags'),Field('material', 'upload', uploadfolder="uploads/"),
                    Field('dislaimer', 'boolean', requires=IS_EQUAL_TO("on", error_message="Please read the disclaimer")))
   
    form = SQLFORM.factory(*form_content)
    
    response.flash = "You are the Whistleblower"
    
    if form.accepts(request.vars, session):
        l = request.vars
        leak_id = gl.create_leak(l.Title, l.Description, None, None,
                {"Al Jazeera":10 , "CNN":20, "Leaker":0}, l.Tags)
        
        #response.flash = 'form accepted'
        leak = Leak(leak_id)

        #FIXME do this better...
        tulips = []
        for tulip in leak.tulips:
            if tulip.target=="Leaker":
                leaker_tulip = tulip.url
            else:
                tulips.append((tulip.url, tulip.target))
            
        return dict(leak_id=leak_id, tulip=leaker_tulip, form=None, tulips=tulips)
    elif form.errors:
        response.flash = 'form has errors'
    
    return dict(form=form, leak_id=None, tulip=None, tulips=None)
