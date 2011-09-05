#!/usr/bin/env python
import time,os
import zipfile, tempfile
# from boto.ses.connection import SESConnection

MimeMail = local_import('mailer').MultiPart_Mail(settings)
MessageContent = local_import('mailer').MessageContent()

# conn = SESConnection(settings.aws_key, settings.aws_secret_key) 

fp = open("/tmp/cron.log", "a+")
fp.write(time.ctime()+"\n")

"""if(db.auth_user):
    # XXX Remove for non demo usage
    if(not db(db.auth_user.email=="node@globaleaks.org").select().first()):
        db.auth_user.insert(first_name="Globaleaks node administrator",
                            last_name="Globaleaks",email="node@globaleaks.org",
                            password=db.auth_user.password.validate("testing"))"""


new_material = db(db.leak.spooled==False).select()


"""for mat in new_material:
    if db(db.material.leak_id==mat.id).select():
        mat_dir = os.path.join(request.folder, 'material/') + str(mat.id)
        fp.write("mat_dir %s\n" % mat_dir)

        fp.write("path %s\n" % os.path.join(mat_dir, str(mat.id)+".zip"))
        zip = zipfile.ZipFile(mat_dir+".zip", 'w')
        fp.write("zip %s\n" % zip)

        for file in os.listdir(mat_dir):
            zip.write(mat_dir+"/"+file, file)

        zip.close()
        db.leak[mat.id].update_record(spooled=True)
        db.commit()"""


mails = db(db.mail).select()

fp.write(str(mails)+"\n")
if not mail:
    fp.write(time.ctime()+": NO MAILS TO SEND!\n")

for m in mails:
    context = dict(name=m.target,
                    sitename=settings.sitename,
                    tulip_url=m.tulip,
                    site=settings.hostname)
    fp.write(str(dir(response))+"\n")
    fp.write(str(dir(response.render))+"\n")
    message_txt = MessageContent.txt(context)
    message_html = MessageContent.html(context) 

    # XXX Use for AWS
    # conn.send_email(source='node@globaleaks.org', subject='GlobaLeaks notification for:' + m.target, body=message, to_addresses=m.address, cc_addresses=None, bcc_addresses=None, format='text', reply_addresses=None, return_path=None)
    
    to = m.target + "<" + m.address + ">"
    subject = "[GlobaLeaks] A TULIP from node " + settings.sitename + " for " + m.target + " - " + m.tulip[-8:]
    fp.write("Sending to %s\n" % m.target)

    if MimeMail.send(to=to, subject=subject, 
            message_text=message_txt, 
            message_html=message_html):
            db(db.mail.id==m.id).delete()
    
    #mail.send(to=m.address,subject="GlobaLeaks notification for: " + m.target,message=message)
    
fp.close()

db.commit()
