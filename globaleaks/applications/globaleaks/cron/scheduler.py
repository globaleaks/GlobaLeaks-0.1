#!/usr/bin/env python
"""
This is used to spool tulips send them to targets and
perform operations related to the health and wellbeing of
a GlobaLeaks node
"""

import time
# from boto.ses.connection import SESConnection

MimeMail = local_import('mailer').MultiPart_Mail(settings)
MessageContent = local_import('mailer').MessageContent()
logger = local_import('logger').start_logger(settings.logging)
compressor = local_import('compress_material').Zip()

# conn = SESConnection(settings.aws_key, settings.aws_secret_key)

logger.info('### Starting GlobaLeaks at: %s ###',  time.ctime())

# Create first node administrator
if db.auth_user:
    # XXX Remove for non demo usage
    if not db(db.auth_user.email=="node@globaleaks.org").select().first():
        db.auth_user.insert(
            first_name="Globaleaks node administrator",
            last_name="Globaleaks",
            email="node@globaleaks.org",
            password=db.auth_user.password.validate("testing")[0])
        logger.info("First launch of GlobaLeaks, creating node administrator!")
        db.commit()

unspooled = db(db.leak.spooled!=True).select()
logger.info("New material: %s : ", unspooled)

for submission in unspooled:
    compressor.create_zip(db, submission, request, logger)
    db.leak[submission.id].update_record(spooled=True)
    logger.info(submission)
    db.commit()

mails = db(db.mail).select()
logger.info(str(mails)+"\n")

#if not mails:
#    logger.info(time.ctime()+": NO MAILS TO SEND!\n")

for m in mails:
    context = dict(name=m.target,
                    sitename=settings.globals.sitename,
                    tulip_url=m.tulip,
                    site=settings.private.hostname)

    message_txt = MessageContent.txt(context)
    message_html = MessageContent.html(context)
    print message_html

    # XXX Use for AWS
    # conn.send_email(source='node@globaleaks.org', \
    #     subject='GlobaLeaks notification for:' + m.target,\
    #     body=message, to_addresses=m.address, cc_addresses=None, \
    #     bcc_addresses=None, format='text', reply_addresses=None, \
    #     return_path=None)

    to = m.target + "<" + m.address + ">"
    subject = "[GlobaLeaks] A TULIP from node %s for %s - %s" % (
              settings.globals.sitename, m.target, str(m.tulip[-8:]))
    logger.info("Sending to %s\n", m.target)

    if MimeMail.send(to=to, subject=subject,
                     message_text=message_txt,
                     message_html=message_html):
        db(db.mail.id==m.id).delete()

    # XXX Uncomment in real world environment
    # mail.send(to=m.address,subject="GlobaLeaks notification for: " + \
    #    m.target,message=message)
    db(db.mail.id==m.id).delete()

db.commit()
