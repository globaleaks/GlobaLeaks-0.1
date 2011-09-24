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

def access_increment(t):

    if t.accesses_counter:
        new_count = int(t.accesses_counter) + 1            
        db.tulip[t.target].update_record(accesses_counter=new_count)
    else:
        db.tulip[t.target].update_record(accesses_counter=1)
     
    if(int(t.allowed_accesses) != 0 and int(t.accesses_counter) > int(t.allowed_accesses)):
        return True
    else:
        return False
    
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
    # handle target page management
    target_url = "FIXME FIXME"

    access_available = access_increment(t)
    
    if whistleblower == False:
        download_available = (int(t.allowed_downloads) == 0 or int(t.downloads_counter) > int(t.allowed_downloads))
    else:
        download_available = False
 
    return dict(err=None,
            access_available=access_available,
            download_available=download_available,
            whistleblower=whistleblower,
            tulip_url=tulip_url,
            leak_id=leak.id,
            leak_title=leak.title,
            leak_tags=leak.tags,
            leak_desc=leak.desc,
            leak_material=leak.material,
            tulip_accesses=t.accesses_counter,
            tulip_allowed_accesses=t.allowed_accesses,
            tulip_download=t.downloads_counter,
            tulip_allowed_download=t.allowed_downloads,
            name=t.target,
            target_url=target_url,
            targets=gl.get_targets("ANY"))

def download_increment(t):

    if(int(t.allowed_downloads) !=0 and int(t.downloads_counter) > int(t.allowed_downloads)):
        return True
   
    if t.downloads_counter:
        new_count = int(t.downloads_counter) + 1            
        db.tulip[t.target].update_record(downloads_counter=new_count)
    else:
        db.tulip[t.target].update_record(downloads_counter=1)

    return False

def download():
    import os

    tulip_url = request.args[0]

    try:
        t = Tulip(url=tulip_url)
    except:
        redirect("/tulip/" + tulip_url);
    
    target = gl.get_target(t.target)

    if(download_increment(t)):
        redirect("/tulip/" + tulip_url);
 
    leak = t.get_leak()
    
    response.headers['Content-Type'] = "application/octet"
    response.headers['Content-Disposition'] = 'attachment; filename="' + tulip_url + '.zip"'
    
    return response.stream(open(os.path.join(request.folder, 'material/', 'static.zip'),'rb'))
