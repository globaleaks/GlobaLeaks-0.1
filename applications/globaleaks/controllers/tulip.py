def index():

    import hashlib
    tulip_url = None
    
    
    form = SQLFORM.factory(Field('Receipt', requires=IS_NOT_EMPTY()))
    
    
    if form.accepts(request.vars, session):
        l = request.vars
        tulip_url = hashlib.sha256(l.Receipt).hexdigest()
        return dict(tulip_url=tulip_url, form=None)

    return dict(form=form,tulip_url=tulip_url)

def status():
    tulip_url = request.args[0]
    
    try:
        t = Tulip(url=tulip_url)
    
    except:
        return dict(err=True)

    leak = t.get_leak()
    
    if t.target == "0":
        whistleblower=True
        response.flash = "You are the Whistleblower"
    else:
        whistleblower=False
        response.flash = "You are the Target"
    
    dead = False
    
    form = SQLFORM.factory(Field('Comment', 'text', requires=IS_NOT_EMPTY()))

    if(int(t.downloads_counter) >= int(t.allowed_downloads) and int(t.allowed_downloads)!=0):
        dead = True
    else:
        t.downloads_counter = int(t.downloads_counter) + 1

    if form.accepts(request.vars, session):
        response.flash = 'ok!'
        c = response.vars

        return dict(err=None,
                dead=dead,
                whistleblower=whistleblower,
                tulip_url=tulip_url,
                leak_id=leak.id,
                leak_title=leak.title,
                leak_tags=leak.tags,
                leak_desc=leak.desc,
                leak_material=leak.material,
                tulip_downloads=t.downloads_counter,
                tulip_allowed_downloads=t.allowed_downloads,
                comment="asdads", 
                name=t.target, 
                comment_form=form)

    elif form.errors:
        response.flash = 'form has errors'

   
    return dict(err=None,
                dead=dead,
                whistleblower=whistleblower,
                leak_id=leak.id,
                tulip_url=tulip_url,
                leak_title=leak.title,
                leak_tags=leak.tags,
                leak_desc=leak.desc,
                leak_material=leak.material,
                tulip_downloads=t.downloads_counter,
                tulip_allowed_downloads=t.allowed_downloads,
                comment_form=form,
                comment=None)

def download():
    tulip_url = request.args[0]
    import os
    try:
        t = Tulip(url=tulip_url)
    except:
        return dict(err=True)
    
    leak = t.get_leak()
    
    response.headers['Content-Type'] = "application/octet"
    response.headers['Content-Disposition'] = 'attachment; filename="' + tulip_url + '.zip"'
    
    return response.stream(open(os.path.join(request.folder, 'material/', str(leak.id)+'.zip'),'rb'))
