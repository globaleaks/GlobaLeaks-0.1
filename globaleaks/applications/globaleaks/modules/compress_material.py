import zipfile
import os

class Zip:
    """
    Class that creates the material archive.
    """
    def create_zip(self, db, mat, request, logger):
        """
        Function to create an unencrypted zipfile
        """
        if db(db.material.leak_id==mat.id).select():
            fldr = str(db(db.submission.leak_id==mat.id).select(
                      db.submission.dirname).first().dirname)
            mat_dir = os.path.join(request.folder, 'material/') + fldr
            logger.info("mat_dir %s\n", mat_dir)
            logger.info("path %s\n",
                        os.path.join(mat_dir, fldr + ".zip"))
            zipf = zipfile.ZipFile(mat_dir+".zip", 'w')

            for f in os.listdir(mat_dir):
                zipf.write(mat_dir+"/"+f, f)

            zipf.close()
            db.leak[mat.id].update_record(spooled=True)
            db.commit()

    def create_encrypted_zip():
        pass
