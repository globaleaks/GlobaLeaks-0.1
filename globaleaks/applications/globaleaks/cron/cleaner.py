#!/usr/bin/env python
"""
This is used to clean expired Tulips and broken uploads
"""
import sys
import os
import time
import stat
import datetime
# from boto.ses.connection import SESConnection

from gluon.utils import md5_hash
from gluon.restricted import RestrictedError
from config import projroot

# useful init
logger = local_import('logger').start_logger(settings.logging)

# expired tulip removal
tulipsexpire = settings.globals.expire_days

total_submissions = db(db.leak.ALL).select()
for submissions in total_submissions:
    print submissions.submission_timestamp, spooled


pass
# -----
# conn = SESConnection(settings.aws_key, settings.aws_secret_key)

logger.info('### Starting GlobaLeaks at: %s ###',  time.ctime())

unspooled = db(db.leak.spooled!=True).select()
logger.info("New material: %s : ", unspooled)

for leak_to_spool in unspooled:
    leak = Leak(leak_to_spool.id)
    submission = db(db.submission.leak_id==leak_to_spool.id).select().first()
    if submission.dirname and not randomizer.is_human_dirname(submission.dirname):
        human_dirname = randomizer.generate_human_dirname(request,
                                                          leak,
                                                          submission.dirname)
        os.rename(os.path.join(request.folder, "material", submission.dirname),
                  os.path.join(request.folder, "material", human_dirname))
        db(db.submission.id == submission.id).update(dirname=human_dirname)
    if submission.dirname:
        human_path = os.path.join(request.folder, "material", submission.dirname)
        compressor.create_zip(db, leak_to_spool, request, logger)
        compressor.create_zip(db, leak_to_spool, request, logger, no_subdirs=True)
        first = True
        for directory in os.walk(human_path):
            if not first:
                mat_dir = directory[0]
                compressor.create_zip(db, leak_to_spool, request, logger,
                                      None, mat_dir)
            first = False
    db.leak[leak_to_spool.id].update_record(spooled=True)
    logger.info(leak_to_spool)
    db.commit()

mails = db(db.mail).select()
logger.info(str(mails)+"\n")

for m in mails:
    context = dict(name=m.target,
                    sitename=settings.globals.sitename,
                    tulip_url=m.tulip,
                    site=settings.globals.baseurl,
                    sitehs=settings.globals.hsurl)

    message_txt = MimeMail.make_txt(context)
    message_html = MimeMail.make_html(context)

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

    #if MimeMail.send(to=m.address, subject=subject,
    #                 message_text=message_txt,
    #                 message_html=message_html):
    if mail.send(to=m.address, subject=subject,
                    message=(message_txt, message_html)):

        logger.info("email sent.")
        db(db.mail.id==m.id).delete()
    else:
        logger.info("error in sending mail.")

    # XXX Uncomment in real world environment
    # mail.send(to=m.address,subject="GlobaLeaks notification for: " + \
    #    m.target,message=message_html)


path = os.path.join(projroot, 'globaleaks',
                    'applications', 'globaleaks', 'errors')

hashes = {}

### CONFIGURE HERE
ALLOW_DUPLICATES = True
### END CONFIGURATION

if settings.globals.debug_notification:
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
            message += "<h2>LOCALS: </h2><br> %s<br><br>" % error.snapshot['locals']
            message += "<h2>REQUEST: </h2><br> %s<br><br>" % error.snapshot['request']
            message += "<h2>SESSION:</h2><br>  %s<br><br>" % error.snapshot['session']
        except KeyError:
            pass

        if MimeMail.send(to=settings.globals.debug_email, subject='new web2py ticket',
                         message_text=message,
                         message_html=message):
            logger.info("... email sent.")
            if settings.globals.debug_deletetickets:
                os.unlink(filename)

    # xxx: should be removed, and used as soon as it becomes necessary
    db.commit()