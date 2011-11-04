#!/usr/bin/env python
#
# Port of jQuery File Upload Plugin PHP example in web2py Python
#
# Original code
# Copyright 2010, Sebastian Tschan
# https://blueimp.net
#
# Licensed under the MIT license:
# http://creativecommons.org/licenses/MIT/


import os
import urllib
import shutil
import time

class UploadHandler:
    def __init__(self, options=None):
        self.__options = {
                    'script_url' : request.env.path_info,
                    'upload_dir': request.folder + 'uploads', # Maybe this
                    'upload_url': '', # .. and this should removed?
                    'param_name': 'files[]',
                    'max_file_size': None,
                    'min_file_size': 1,
                    'accept_file_types': 'ALL',
                    'max_number_of_files': None,
                    'discard_aborted_uploads': True,
                    'chunksize': None,
                    'image_versions': {
                                    'thumbnail': {
                                                'upload_dir': request.folder + '/thumbnails/',
                                                'upload_uri': request.env.path_info + '/thumbnails/',
                                                'max_width': 80,
                                                'max_height': 80
                                                }
                                    }
                    }
        if options:
            self.__options = options

    def __get_file_object(self, file_name):
        file_path = os.path.join(self.__options['upload_dir'], file_name)
        if not os.path.isfile(file_path) and file_name[0] != '.':
            f = open(file_path, 'w')
            f.write('')
            f.close()

        if os.path.isfile(file_path) and file_name[0] != '.':
            file = Storage()
            file.name = file_name
            file.size = os.path.getsize(file_path)

            file.url = "#"
            #file.url = self.__options['upload_url'] + \
            #        file.name.replace(' ', '%20')
#           for version, options in self.__options['image_versions']:
#               if os.path.isfile(self.__options['upload_dir'] + file_name):
#                   file[version + '_url'] = options['upload_url'] + \
#                                       urllib.urlencode(file.name)

            file.delete_url = self.__options['script_url'] + \
                            "?deletefile=" + file.name.replace(' ','%20')

            file.delete_type = 'GET'

            return response.json([dict(**file)])

        return None

    def __get_file_objects(self):
        files = []
        for file in os.listdir(self.__options['upload_dir']):
            files.append(self.__get_file_object(file))
        return files

    def __create_scaled_image(self, file_name, options):
        # Function unimplemented because not needed by GL
        return True

    def __has_error(self, uploaded_file, file, error):
        if error:
            return error

        if file.name.split['.'][-1:][0] not in \
                self.__options['accepted_file_types'] and \
                self.__options['accepted_file_types'] != "ALL":
            return 'acceptFileTypes'

        if self.__options['max_file_size'] and \
            (file_size > self.__options['max_file_size'] or \
                file.size > self.__options['max_file_size']):
            return 'maxFileSize'

        if self.__options['min_file_size'] and \
            file_size > self.__options['min_file_size']:
            return 'minFileSize'

        if self.__options['max_number_of_files'] and \
            int(self.__options['max_number_of_files']) <= \
                len(self.__get_file_objects):
            return 'maxNumberOfFiles'

        return None

    def __handle_file_upload(self, uploaded_file, name, size, type, error):
        file = Storage()

        # checking name duplicates and in case change filename
        if os.path.exists(os.path.join(request.folder, 'material',
                                       self.get_file_dir(), name)):
            name = "%s%s.%s" % ("".join(name.split(".")[:-1]),
                                int(time.time()),
                                name.split(".")[-1])
        print name


        file.name = os.path.basename(name).strip('.\x20\x00..')
        #file.name = strip_path_and_sanitize(name)
        file.size = int(size)
        file.type = type
        file.id = randomizer.alphanumeric(20)

        # error = self.__has_error(uploaded_file, file, error)
        error = None

        if not error and file.name:
            file_path = os.path.join(self.__options['upload_dir'], file.name)
            # print "filepath: %s " % file_path
            append_file = not self.__options['discard_aborted_uploads'] and os.path.isfile(file_path) and file.size > os.path.getsize(file_path)
            # print "append: %s file.size: %s getsize: %s" % (append_file, file.size, os.path.getsize(file_path))

            # print "file position: %s" % (uploaded_file.tell())

            if uploaded_file:
            # multipart/formdata uploads (POST method uploads)
                if append_file:
                    dst_file = open(file_path, 'ab')
                    shutil.copyfileobj(
                                    uploaded_file,
                                    dst_file
                                    )
                else:
                    dst_file = open(file_path, 'w+b')
                    shutil.copyfileobj(
                                    uploaded_file,
                                    dst_file
                                    )
            else:
            # Non-multipart uploads (PUT method)
            # take the request.body web2py file stream
                if append_file:
                    shutil.copyfileobj(
                                    request.body,
                                    open(file_path, 'ab')
                                    )
                else:
                    shutil.copyfileobj(
                                    request.body,
                                    open(file_path, 'w+b')
                                    )
            file_size = os.path.getsize(file_path)

            if file_size == file.size or not request.env.http_x_file_name:
                #file.url = self.__options['upload_url'] + file.name.replace(" ", "%20")
                file.url = "#"

#               for version, options in self.__options['image_versions']:
#                   if os.path.isfile(self.__options['upload_dir'] + file_name):
#                       file[version + '_url'] = self.__options['upload_url'] + \
#                                           urllib.urlencode(file.name)

            elif self.__options['discard_aborted_uploads']:
                os.remove(file_path)
                file.error = 'abort'

            if request.env.http_x_file_size:
                file.size = int(request.env.http_x_file_size)
            else:
                file.size = file_size

            file.delete_url = self.__options['script_url'] + \
                        "?deletefile=" + file.name.replace(" ", "%20")

            file.delete_type = 'GET'

        else:
            file.error = error

        return response.json([dict(**file)])

    def get_file_dir(self):
        filedir = db(db.submission.session ==
                     session.wb_id).select().first()

        if not filedir:
            if not session.dirname:
                filedir = randomizer.generate_dirname()
                session.dirname = filedir
            else:
                filedir = session.dirname
        else:
            filedir = str(filedir.dirname)

        return filedir

    def get(self):
        if request.vars.file:
            file_name = os.path.basename(request.vars.file)
            #file_name = strip_path_and_sanitize(request.vars.file)
            info = self.__get_file_object(file_name)
        else:
            filename = None
            info = self.__get_file_objects()
        return info

    def post(self):
        upload = Storage()
        upload['error'] = False

        if request.env.http_x_file_name:
            info = self.__handle_file_upload(
                                        request.body,
                                        request.env.http_x_file_name,
                                        request.env.http_x_file_size,
                                        request.env.http_x_file_type,
                                        upload['error']
                                        )
            return info
        elif request.vars:
            try:
                upload.data = request.vars[self.__options['param_name']]
            except:
                return dict(error=True)
            upload['size'] = False #upload.data.file.tell()
            upload['type'] = upload.data.type
            upload.name = upload.data.filename
            # upload['file'] = upload_file.file
            # For the moment don't handle multiple files in one POST
            info = self.__handle_file_upload(
                                        upload.data.file,
                                        upload['name'],
                                        upload['size'],
                                        upload['type'],
                                        upload['error']
                                        )
            return info

        return dict(error=True)

    def delete(self):
        file_name = os.path.basename(request.vars.deletefile) if request.vars.deletefile else None
        file_path = os.path.join(request.folder,'material',self.get_file_dir(),file_name)
        success = os.path.isfile(file_path) and file_name[0] != "." and os.remove(file_path)
        if success:
            return {'result': 'success'}
        else:
            return {'result': 'fail'}

