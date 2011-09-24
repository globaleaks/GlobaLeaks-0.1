import zipfile
import os

class Zip:
    """
    Class that creates the material archive.
    """
    def create_zip(self, db, mat, logger):
        """
        Function to create an unencrypted zipfile
        """
        if db(db.material.leak_id==mat.id).select():
            fldr = db(db.submission.session==session.wb_id).select(
                      db.submission.dirname).first()
            mat_dir = os.path.join(request.folder, 'material/') + fldr
            self.logger.info("mat_dir %s\n", mat_dir)
            self.logger.info("path %s\n",
                             os.path.join(mat_dir, fldr + ".zip"))
            zipf = zipfile.ZipFile(mat_dir+".zip", 'w')
            self.logger.info("zip %s\n", zipf)

            for f in os.listdir(mat_dir):
                zip.write(mat_dir+"/"+f, f)

            zipf.close()
            self.db.leak[self.mat.id].update_record(spooled=True)
            self.db.commit()

    def create_encrypted_zip():
        pass
