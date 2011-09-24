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

# this is called only in the Target context
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
    
    if whistleblower == False:
    # the stats of the whistleblower stay in the tulip entry (its unique!)
        download_available = (int(t.allowed_downloads) == 0 or int(t.downloads_counter) > int(t.allowed_downloads))
        access_available = access_increment(t)
        counter_accesses = t.accesses_counter
        limit_counter = t.allowed_accesses
    else:
    # the stats of the whistleblower stay in the leak/material entry
        download_available = False
        if leak.whistleblower_access:
            new_count = int(leak.whistleblowing_access) + 1            
            leak.whistleblower_access=new_count
        else:
            leak.whistleblower_counter=1
            
        counter_accesses = leak.whistleblower_access   
        limit_counter = int("50") # settings.max_submitter_accesses 
        access_available = True 
 
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
            tulip_accesses=counter_accesses,
            tulip_allowed_accesses=limit_counter,
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
