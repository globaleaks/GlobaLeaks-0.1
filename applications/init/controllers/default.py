# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call():
    session.forget()
    return service()
### end requires
def index():
    return dict(message=T("Hello World, I am GlobaLeaks!"))

def submission():
    form_content = (Field('Title', requires=IS_NOT_EMPTY()),
                    Field('Description', 'text', requires=IS_NOT_EMPTY()),
                    Field('Tags'),Field('material', 'upload', uploadfolder="uploads/"),
                    Field('dislaimer', 'boolean', requires=IS_EQUAL_TO("on", error_message="Please read the disclaimer")))
   
    form = SQLFORM.factory(*form_content)
    
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
            
        return dict(leak_id=leak_id, tulip=tulip.url, form=None, tulips=tulips)
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'        
    
    return dict(form=form, leak_id=None, tulip=None, tulips=None)

def tulip():
    tulip_url = request.args[0]
    t = Tulip(url=tulip_url)
    leak = t.get_leak()
    
    if(int(t.downloads_counter) >= int(t.allowed_downloads)):
        return dict(dead=True,
                leak_title=leak.title,
                leak_tags=leak.tags,
                leak_desc=leak.desc,
                leak_material=leak.material,
                tulip_downloads=t.downloads_counter,
                tulip_allowed_downloads=t.allowed_downloads)
    t.downloads_counter = int(t.downloads_counter) + 1
    
    return dict(dead=False,
                leak_title=leak.title,
                leak_tags=leak.tags,
                leak_desc=leak.desc,
                leak_material=leak.material,
                tulip_downloads=t.downloads_counter,
                tulip_allowed_downloads=t.allowed_downloads)

def error():
    return dict()
