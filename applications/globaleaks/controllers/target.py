def index(): return dict(message="hello from target.py")

def subscribe():
    if not request.args:
        subscribe_form = SQLFORM.factory(
                            Field('Name', requires=IS_NOT_EMPTY()),
                            Field('Email', requires=IS_NOT_EMPTY()),
                            Field('Description','text', requires=IS_NOT_EMPTY())
                                )
        if subscribe_form.accepts(request.vars, session):
            return dict(message="Not implemented!",subscribe=None)
            
        return dict(message="Here you can subscribe as a target",subscribe=subscribe_form)
        
    if request.args:
        tulip_url = request.args[0]
    else:
        tulip_url = None
            
    try:
        tulip = Tulip(url=tulip_url)
    except:
        return dict(message="Error!",subscribe=None)
    
    if not tulip_url or tulip.target == "0":
        return dict(message="Error!",subscribe=None)
        
    else:
        target = db(db.target.id==tulip.target).select().first()
        
        if not target:
            return dict(message="Error!",subscribe=None)

        if target.status == "subscribed":
            return dict(message="already subscribed",subscribe=None)

        else:
            db.target[tulip.target].update_record(status="subscribed")
            return dict(message="subscribed",subscribe=None)
            
    return dict(message="this is logically impossible",subscribe=None)

def unsubscribe():
    if request.args:
        tulip_url = request.args[0]
    else:
        tulip_url = None
            
    try:
        tulip = Tulip(url=tulip_url)
    except:
        return dict(message="Error!")
    
    if not tulip_url or tulip.target == "0":
        return dict(message="Error!")
        
    else:
        target = db(db.target.id==tulip.target).select().first()
        
        if not target:
            return dict(message="Error!")
        
        if target.status == "unsubscribed":
            return dict(message="already unsubscribed")

        else:
            db.target[tulip.target].update_record(status="unsubscribed")
            return dict(message="unsubscribed")
            
    return dict(message="this is logically impossible")
