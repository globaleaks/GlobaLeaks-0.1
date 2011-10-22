import zipfile
import os.path
import subprocess

from os import listdir

class Zip:
    """
    Class that creates the material archive.
    """
    def create_zip(self, db, submission, request, logger, passwd=None):
        """
        Function to create an unencrypted zipfile
        """
        if db(db.material.leak_id==submission.id).select().first():
            try:
                filedir = str(db(db.submission.leak_id==submission.id).select(
                          db.submission.dirname).first().dirname)
            except:
                logger.error('create_zip: invalid filedir')
                return dict(error='invalid filedir')

            try:
                mat_dir = os.path.join(request.folder, 'material/') + filedir
                logger.info('mat_dir %s', mat_dir)
                logger.info('path %s',
                            os.path.join(mat_dir, filedir + '.zip'))
                # XXX: issue #51
                if passwd and os.path.exists(mat_dir):
                    cmd = 'zip -e -P%(passwd) %(zipfile).zip %(files)' % dict(
                           passwd = passwd, zipfile=matdir,
                           files = ' '.join(listdir(mat_dir)))
                    subprocess.check_call(cmd.split())
                elif not passwd and os.path.exists(mat_dir):
                    zipf = zipfile.ZipFile(mat_dir+'.zip', 'w')
                    for f in listdir(mat_dir):
                        zipf.write(os.path.join(mat_dir, f), f)
                else:
                    logger.error('create_zip: invalid path')
            except RuntimeError as err:
                logger.error('create_zip: error in creating zip')
                try:
                    zipf.close()
                except (RuntimeError, zipfile.error) as err:
                    logger.info('create_zip: error when trying to save zip')
            except subprocess.CalledProcessError as err :
                    logger.error('create_zip: error in creating zip')
            else:
                err = None
            finally:
                return dict(error=err) if err else None
