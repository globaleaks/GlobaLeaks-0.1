#!/usr/bin/env python
"""
This is used to spool tulips send them to targets and
perform operations related to the health and wellbeing of
a GlobaLeaks node
"""
import sys
import os
import time
import stat
import datetime
# from boto.ses.connection import SESConnection

MimeMail = local_import('mailer').MultiPart_Mail(settings)
MessageContent = local_import('mailer').MessageContent()
logger = local_import('logger').start_logger(settings.logging)
compressor = local_import('compress_material').Zip()

# conn = SESConnection(settings.aws_key, settings.aws_secret_key)

logger.info('### Starting GlobaLeaks at: %s ###',  time.ctime())

# Create first node administrator
#FIXME Remove for non demo usage
if db.auth_user:
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
    #    m.target,message=message_html)
    db(db.mail.id==m.id).delete()

from gluon.utils import md5_hash
from gluon.restricted import RestrictedError
from gluon.tools import Mail

path = os.path.join(os.getcwd(), 'applications/globaleaks/errors/')

hashes = {}

### CONFIGURE HERE
ALLOW_DUPLICATES = True
### END CONFIGURATION

logger.info("DIR: %s" % os.listdir(path))
for file in os.listdir(path):
    filename = os.path.join(path, file)

    if not ALLOW_DUPLICATES:
        file_data = open(filename, 'r').read()
        key = md5_hash(file_data)

        if key in hashes:
            continue

        hashes[key] = 1

    error = RestrictedError()
    error.load(request, request.application, filename)
    logger.info("err_traceback: %s", error.traceback)

    mail.send(to="hellais@gmail.com", 
              subject='new web2py ticket', 
              message=error.traceback)
    
    os.unlink(filename)


db.commit()
