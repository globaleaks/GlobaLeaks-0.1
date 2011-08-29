# coding: utf8
# try something like
def index(): return dict(message="hello from target.py")


def subscribe():
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
        
        if target.status == "subscribed":
            return dict(message="already subscribed")

        else:
            db.target[tulip.target].update_record(status="subscribed")
            return dict(message="subscribed")
            
    return dict(message="this is logically impossible")



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
        
        
        if target.status == "unsubscribed":
            return dict(message="already unsubscribed")

        else:
            db.target[tulip.target].update_record(status="unsubscribed")
            return dict(message="unsubscribed")
            
    return dict(message="this is logically impossible")
