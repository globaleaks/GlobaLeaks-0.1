import zipfile
import os

class Zip:
    """
    Class that creates the material archive.
    """
    def create_zip(self, db, submission, request, logger):
        """
        Function to create an unencrypted zipfile
        """
        if db(db.material.leak_id==submission.id).select().first():
            try:
                filedir = str(db(db.submission.leak_id==submission.id).select(
                          db.submission.dirname).first().dirname)
            except:
                logger.error("create_zip: invalid filedir")
                return dict(error='invalid filedir')
            
            mat_dir = os.path.join(request.folder, 'material/') + filedir
            logger.info("mat_dir %s\n", mat_dir)
            logger.info("path %s\n",
                        os.path.join(mat_dir, filedir + ".zip"))
            zipf = zipfile.ZipFile(mat_dir+".zip", 'w')
            if mat_dir:
                for f in os.listdir(mat_dir):
                    zipf.write(mat_dir+"/"+f, f)

            zipf.close()

    def create_encrypted_zip():
        pass
