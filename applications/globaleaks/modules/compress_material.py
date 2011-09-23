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
        mat_dir = os.path.join(request.folder, 'material/') + str(self.mat.id)
        self.logger.info("mat_dir %s\n", mat_dir)
        self.logger.info("path %s\n",
                         os.path.join(mat_dir, str(self.mat.id)+".zip"))
        zipf = zipfile.ZipFile(mat_dir+".zip", 'w')
        self.logger.info("zip %s\n", zipf)

        for file in os.listdir(mat_dir):
            zip.write(mat_dir+"/"+file, file)

        zipf.close()
        self.db.leak[self.mat.id].update_record(spooled=True)
        self.db.commit()

    def create_encrypted_zip():
        pass
