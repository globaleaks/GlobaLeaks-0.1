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

    message_txt = MimeMail.make_txt(context)
    message_html = MimeMail.make_html(context)
    print message_html

    # XXX Use for AWS
    # conn.send_email(source='node@globaleaks.org', \
    #     subject='GlobaLeaks notification for:' + m.target,\
    #     body=message, to_addresses=m.address, cc_addresses=None, \
    #     bcc_addresses=None, format='text', reply_addresses=None, \
    #     return_path=None)

    to = m.target + " <" + m.address + ">"
    subject = "[GlobaLeaks] A TULIP from node %s for %s - %s" % (
              settings.globals.sitename, m.target, str(m.tulip[-8:]))
    logger.info("Sending to %s\n", m.target)

    if MimeMail.send(to=m.address, subject=subject,
                     message_text=message_txt,
                     message_html=message_html):

        logger.info("email sent.")
        db(db.mail.id==m.id).delete()
    else:
        logger.info("error in sending mail.")

    # XXX Uncomment in real world environment
    # mail.send(to=m.address,subject="GlobaLeaks notification for: " + \
    #    m.target,message=message_html)

from gluon.utils import md5_hash
from gluon.restricted import RestrictedError
from gluon.tools import Mail

path = os.path.join(os.getcwd(), 'applications/globaleaks/errors/')

hashes = {}

### CONFIGURE HERE
ALLOW_DUPLICATES = True
### END CONFIGURATION
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
    logger.info("REQUEST-APP: %s" % dir(request))

    logger.info("Sending email...")

    message = '<b>There has been an error on a node.</b><br>'
    message += '<h1>This is the trackback:</h1><br><pre>%s</pre><br><br><br>' % error.traceback
    message += "<h1>this is the environment:</h1><br>"
    try:
        message += "<h2>RESPONSE: </h2><br> %s<br><br>" % error.snapshot['response']
    except KeyError:
        pass
    try:
        message += "<h2>LOCALS: </h2><br> %s<br><br>" % error.snapshot['locals']
    except KeyError:
        pass
    try:
        message += "<h2>REQUEST: </h2><br> %s<br><br>" % error.snapshot['request']
    except KeyError:
        pass
    try:
        message += "<h2>SESSION:</h2><br>  %s<br><br>" % error.snapshot['session']
    except KeyError:
        pass

    if MimeMail.send(to=settings.globals.debug_email, subject='new web2py ticket',
                     message_text=message,
                     message_html=message):

        logger.info("... email sent.")

        os.unlink(filename)


db.commit()
