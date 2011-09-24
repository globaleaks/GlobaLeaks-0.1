#!/usr/bin/env python
"""
This is used to spool tulips send them to targets and
perform operations related to the health and wellbeing of
a GlobaLeaks node
"""

import time
import logging
# from boto.ses.connection import SESConnection

MimeMail = local_import('mailer').MultiPart_Mail(settings)
MessageContent = local_import('mailer').MessageContent()
logger = local_import('logger').get_logger(settings)
compressor = local_import('compress_material').Zip()

# conn = SESConnection(settings.aws_key, settings.aws_secret_key)

logger.info(time.ctime()+"\n")

# Create first node administrator
if(db.auth_user):
    # XXX Remove for non demo usage
    if(not db(db.auth_user.email=="node@globaleaks.org").select().first()):
        db.auth_user.insert(first_name="Globaleaks node administrator",
                            last_name="Globaleaks",email="node@globaleaks.org",
                            password=db.auth_user.password.validate("testing")[0])
        logger.info("First launch of GlobaLeaks, creating node administrator!")

new_material = db(db.leak.spooled==False).select()

for mat in new_material:
    compressor.create_zip(db=db, mat=mat, logger=logger)

mails = db(db.mail).select()
logger.info(str(mails)+"\n")

if not mail:
    logger.info(time.ctime()+": NO MAILS TO SEND!\n")

for m in mails:
    context = dict(name=m.target,
                    sitename=settings.sitename,
                    tulip_url=m.tulip,
                    site=settings.hostname)

    message_txt = MessageContent.txt(context)
    message_html = MessageContent.html(context)

    # XXX Use for AWS
    # conn.send_email(source='node@globaleaks.org', subject='GlobaLeaks notification for:' + m.target, body=message, to_addresses=m.address, cc_addresses=None, bcc_addresses=None, format='text', reply_addresses=None, return_path=None)

    to = m.target + "<" + m.address + ">"
    subject = "[GlobaLeaks] A TULIP from node " + settings.sitename + " for " + m.target + " - " + m.tulip[-8:]
    logger.info("Sending to %s\n", m.target)

    if MimeMail.send(to=to, subject=subject,
            message_text=message_txt,
            message_html=message_html):
            db(db.mail.id==m.id).delete()

    #mail.send(to=m.address,subject="GlobaLeaks notification for: " + m.target,message=message)

db.commit()
