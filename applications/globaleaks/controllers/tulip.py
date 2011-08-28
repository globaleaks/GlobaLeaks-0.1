def index():
    return dict(dead=False,
                leak_title=None,
                leak_tags=None,
                leak_desc=None,
                leak_material=None,
                tulip_downloads=None,
                tulip_allowed_downloads=None,
                comment=None, 
                name=None,
                comment_form=None)

def status():
    tulip_url = request.args[0]
    t = Tulip(url=tulip_url)
    leak = t.get_leak()
    dead = False
    
    form = SQLFORM.factory(Field('Comment', 'text', requires=IS_NOT_EMPTY()))

    if(int(t.downloads_counter) >= int(t.allowed_downloads) and int(t.allowed_downloads)!=0):
        dead = True
    else:
        t.downloads_counter = int(t.downloads_counter) + 1

    if form.accepts(request.vars, session):
        response.flash = 'ok!'
        c = response.vars
        print response.vars

        return dict(dead=dead,
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
    else:
        response.flash = 'please fill the form'    


    return dict(dead=dead,
                leak_title=leak.title,
                leak_tags=leak.tags,
                leak_desc=leak.desc,
                leak_material=leak.material,
                tulip_downloads=t.downloads_counter,
                tulip_allowed_downloads=t.allowed_downloads,
                comment_form=form,
                comment=None)
