def index():
    import hashlib

    tulip_url = None
    
    form = SQLFORM.factory(Field('Receipt', requires=IS_NOT_EMPTY()))

    response.flash = "You are the Whistleblower"
    
    if form.accepts(request.vars, session):
        l = request.vars
        # Make the tulip work well
        leak_number = l.Receipt.replace(' ','')
        tulip_url = hashlib.sha256(leak_number).hexdigest()
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
   
    target = gl.get_target(t.target)

    dead = False
     
    if(int(t.allowed_accesses) != 0 and int(t.accesses_counter) >= int(t.allowed_accesses)):
        dead = True
    else:
        if t.target != "0":
            if target.tulip_counter:
                new_count = int(target.tulip_counter) + 1
            # XXX move to a Target Datamodel
                db.target[t.target].update_record(tulip_counter=new_count)
            else:
                db.target[t.target].update_record(tulip_counter=1)

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
            name=t.target,
            targets=gl.get_targets("ANY"))

def download():
    import os

    tulip_url = request.args[0]

    try:
        t = Tulip(url=tulip_url)
    except:
        redirect("/tulip/" + tulip_url);
    
    target = gl.get_target(t.target)

    if(int(t.downloads_counter) >= int(t.allowed_downloads) and int(t.allowed_downloads)!=0):
        redirect("/tulip/" + tulip_url);
    else:
        if t.target != "0":
            if target.download_counter:
                new_count = int(target.download_counter) + 1
                # XXX move to a Target Datamodel
                db.target[t.target].update_record(download_counter=new_count)
            else:
                db.target[t.target].update_record(download_counter=1)

        t.downloads_counter = int(t.downloads_counter) + 1

    leak = t.get_leak()
    
    response.headers['Content-Type'] = "application/octet"
    response.headers['Content-Disposition'] = 'attachment; filename="' + tulip_url + '.zip"'
    
    return response.stream(open(os.path.join(request.folder, 'material/', 'static.zip'),'rb'))
