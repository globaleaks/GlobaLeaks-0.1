def index():
    import hashlib

    tulip_url = None
    
    form = SQLFORM.factory(Field('Receipt', requires=IS_NOT_EMPTY()))

    response.flash = "You are the Whistleblower"
    
    if form.accepts(request.vars, session):
        l = request.vars
        tulip_url = hashlib.sha256(l.Receipt).hexdigest()
        redirect("/tulip/" + tulip_url)

    return dict(form=form,tulip_url=None)

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
    
    if(int(t.allowed_accesses) !=0 and int(t.accesses_counter) >= int(t.allowed_accesses)):
        dead = True
    else:
        t.accesses_counter = int(t.accesses_counter) + 1

    if(int(t.allowed_downloads) !=0 and int(t.downloads_counter) >= int(t.allowed_downloads)):
        dead = True

    return dict(err=None,
            dead=dead,
            whistleblower=whistleblower,
            tulip_url=tulip_url,
            leak_id=leak.id,
            leak_title=leak.title,
            leak_tags=leak.tags,
            leak_desc=leak.desc,
            leak_material=leak.material,
            tulip_accesses=t.accesses_counter,
            tulip_allowed_accesses=t.allowed_accesses,
            tulip_downloads=t.downloads_counter,
            tulip_allowed_downloads=t.allowed_downloads,
            name=t.target)

def download():
    import os

    tulip_url = request.args[0]

    try:
        t = Tulip(url=tulip_url)
    except:
        redirect("/tulip/" + tulip_url);

    if(int(t.downloads_counter) >= int(t.allowed_downloads) and int(t.allowed_downloads)!=0):
        redirect("/tulip/" + tulip_url);
    else:
        t.downloads_counter = int(t.downloads_counter) + 1

    leak = t.get_leak()
    
    response.headers['Content-Type'] = "application/octet"
    response.headers['Content-Disposition'] = 'attachment; filename="' + tulip_url + '.zip"'
    
    return response.stream(open(os.path.join(request.folder, 'material/', str(leak.id)+'.zip'),'rb'))
