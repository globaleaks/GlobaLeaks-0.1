#!/usr/bin/env python
import time,os
import zipfile, tempfile

fp = open("/tmp/cron.log", "w+")
fp.write(time.ctime()+"\n")


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

base_message = """Hello there I am GlobaLeaks.
There is a fresh new leak waiting for your at:
    http://%s:%s/tulip/%s
        
Take Care,
Random GlobaLeaks Node
"""

for m in mails:
    mail.send(to=m.address,
            subject="GlobaLeaks notification for: " + m.target,
            message=base_message % (settings.hostname, settings.port, m.tulip))
    db(db.mail.id==m.id).delete()

db.commit()
