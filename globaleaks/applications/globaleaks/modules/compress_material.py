import zipfile
import subprocess
import os

class Zip:
    """
    Class that creates the material archive.
    """
    def create_zip(self, db, submission, request, logger, passwd=None,
                   mat_dir=None, no_subdirs=None):
        """
        Function to create an unencrypted zipfile
        """
        if db(db.material.leak_id==submission.id).select().first():
            try:
                filedir = str(db(db.submission.leak_id==submission.id).select(
                          db.submission.dirname).first().dirname)
                filedir = os.path.join(request.folder, "material", filedir)
            except:
                logger.error('create_zip: invalid filedir')
                return dict(error='invalid filedir')
            err = None
            try:
                # XXX should need some refactoring
                if not mat_dir:
                    mat_dir = filedir
                splitted = os.path.split(mat_dir)
                if splitted[-1].isdigit():
                    filedir = "%s-%s" % (splitted[-2], splitted[-1])
                if no_subdirs:
                    save_file = filedir + "-0"
                    # get only files, no subdirectories
                    files = [f for f in os.listdir(mat_dir)
                             if not os.path.isdir(os.path.join(mat_dir, f))]
                else:
                    save_file = filedir
                    files = os.listdir(mat_dir)
                # XXX: issue #51
                if passwd and os.path.exists(mat_dir):
                    logger.error('Encrypted ZIP function disabled, due to security redesign needs')
                    return 0
       #             cmd = 'zip -e -P%(passwd) %(zipfile).zip %(files)' % dict(
       #                    passwd=passwd, zipfile=filedir,
       #                    files=" ".join(files))
       #             subprocess.check_call(cmd.split())
                elif not passwd and os.path.exists(mat_dir):
                    zipf = zipfile.ZipFile(save_file+'.zip', 'w')
                    for f in files:
                        path = os.path.join(mat_dir, f)
                        zipf.write(path, f)
                        subdirs = os.walk(path)
                        for subdir in subdirs:
                            inner_subdir = os.path.split(subdir[0])[-1]
                            if not inner_subdir.isdigit():
                                inner_subdir = ""
                            for subfile in subdir[2]:
                                zipf.write(os.path.join(subdir[0], subfile),
                                           os.path.join(inner_subdir,subfile))
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
            finally:
                return dict(error=err) if err else None
