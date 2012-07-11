#!/usr/bin/env python
"""
This is used to clean expired TULIPs and broken uploads

REMIND: test environment, if you're testing this script start/stopping globaleaks,
change in globaleaks/cron/crontab the timing, using "* *", because web2py start 
his own crontab only if set to run every minute
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

# recursively clean the directories
# shutil.rmtree: we are against you!
def clean_directory(subm_id, absolute_dir):
    removed_file_count = 0

    for submitted_file in os.listdir(absolute_dir):

        absfilename = os.path.join(absolute_dir, submitted_file)
        if os.path.isdir(absfilename):
            removed_file_count += clean_directory(subm_id, absfilename)
            continue

        if os.access(absfilename, os.W_OK):
            removed_file_count += 1
            os.unlink(absfilename)
        else:
            logger.fatal("anomaly in %s: unable to unlink", absfilename)

    logger.debug("related to tulip %d, has been removed %d from [%s]", subm_id, removed_file_count, absolute_dir)
    os.rmdir(absolute_dir)

    return removed_file_count

# useful init
# logger = local_import('logger').start_logger(settings.logging)
# logger = local_import('logger').logger

# tulip removal deadline, converted in seconds
if settings.tulip.expire_days:
    tulipsexpire = int(settings.tulip.expire_days) * (60 * 60 * 24)
else:
    logger.info("Unable to maintain clean GlobaLeaks database! required configuration in globaleaks.conf expire_days field")

total_submissions = db().select(db.leak.ALL)
actual_time = time.time()

for subm_row in total_submissions:

    submission_time = float(subm_row.submission_timestamp)
    print "debug: checking expire seconds: act %d subm %d expire %d" % (actual_time, submission_time, tulipsexpire)

    if actual_time > (submission_time + tulipsexpire):

        tulip_rows = db(db.tulip.leak_id==subm_row.id).select()
        # remember: material contains the description and the list of files
        material_rows = db(db.material.leak_id==subm_row.id).select()
        # submission contains the directory and the compressed version of the files
        file_row = db(db.submission.leak_id==subm_row.id).select().first()

        absdir = os.path.join(projroot, 'globaleaks', 'applications', 'globaleaks', 'material', file_row.dirname)
        logger.info("expired submission id #%d contains %d Tulips, filesystem ref: %s", subm_row.id, len(tulip_rows), absdir)

        # we may have: the /path/globaleaks/material + 'name-stored' [.zip|/],
        # the directory may contains the files uncompressed

        if os.access((absdir + '.zip'), os.W_OK):
            os.unlink(absdir + '.zip')

        file_deleted = 0
        if os.access(absdir, os.X_OK ):
            file_deleted += clean_directory(subm_row.id, absdir)

        # database removal sequence
        db(db.leak.id==subm_row.id).delete()
        db(db.material.leak_id==subm_row.id).delete()
        db(db.submission.leak_id==subm_row.id).delete()

        for single_tulip in tulip_rows:
            db(db.tulip.id==single_tulip.id).delete()
    
        db.commit()


# broken upload checks
