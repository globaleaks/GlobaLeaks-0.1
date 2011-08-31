#!/usr/bin/env python
import time,os
import zipfile, tempfile

fp = open("/tmp/cron.log", "w+")
fp.write(time.ctime()+"\n")

if(db.auth_user):
    # XXX Remove for non demo usage
    if(not db(db.auth_user.email=="node@globaleaks.org").select().first()):
        db.auth_user.insert(first_name="Globaleaks node administrator",
                            last_name="Globaleaks",email="node@globaleaks.org",
                            password=db.auth_user.password.validate("testing"))


new_material = db(db.leak.spooled==False).select()

for mat in new_material:
    if db(db.material.leak_id==mat.id).select():
        mat_dir = os.path.join(request.folder, 'material/') + str(mat.id)
        fp.write("mat_dir %s\n" % mat_dir)
        #zip_tmp = tempfile.TemporaryFile(prefix='material', suffix='.zip')

        fp.write("path %s\n" % os.path.join(mat_dir, str(mat.id)+".zip"))
        zip = zipfile.ZipFile(mat_dir+".zip", 'w')
        fp.write("zip %s\n" % zip)

        for file in os.listdir(mat_dir):
            zip.write(mat_dir+"/"+file, file)

        zip.close()
        db.leak[mat.id].update_record(spooled=True)
        db.commit()
        
fp.close()

mails = db(db.mail).select()

for m in mails:
    message = """Hello there I am GlobaLeaks.
There is a fresh new leak waiting for your at:
    http://%s:%s/tulip/%s
        
Take Care,
Random GlobaLeaks Node

to unsubscribe: http://%s:%s/globaleaks/target/unsubscribe/%s
to subscribe back: http://%s:%s/globaleaks/target/subscribe/%s
""" % (settings.hostname, settings.port, m.tulip,
        settings.hostname, settings.port, m.tulip,
        settings.hostname, settings.port, m.tulip)

    mail.send(to=m.address,
            subject="GlobaLeaks notification for: " + m.target,
            message=message)
    db(db.mail.id==m.id).delete()

db.commit()
