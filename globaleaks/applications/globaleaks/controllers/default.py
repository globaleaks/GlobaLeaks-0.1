### required - do no delete
def user(): 
    return dict(form=auth())

def download(): 
    return response.download(request,db)

def call():
    session.forget()
    return service()
### end requires

def index():
    import hashlib

    tulip_url = None

    if request.vars:
        l = request.vars
        # Make the tulip work well
        leak_number = l.Receipt.replace(' ','')
        tulip_url = hashlib.sha256(leak_number).hexdigest()
        redirect("/tulip/" + tulip_url)

    return dict(tulip_url=None)

def error(): return dict()

def email_template(): return dict()

