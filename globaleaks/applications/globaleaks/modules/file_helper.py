import os

def move(src, dst, cur_folder):
            dst_folder = os.path.join(cur_folder, 'material/' + filedir + '/')

            if not os.path.isdir(dst_folder):
                os.makedirs(dst_folder)
            os.rename(os.path.join(cur_folder, 'uploads/') +
                      tmp_file, dst_folder + filename)