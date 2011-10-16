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


import os, urllib
import shutil

class UploadHandler:
	__options = []

	def __init__(options=None):
		self.options = {
					'script_url' : request.env.path_info,
					'upload_dir': request.folder + '/files', # Maybe this
					'upload_url': request.env.path_info + '/files/', # .. and this should removed?
					'param_name': 'files',
					'max_file_size': None,
					'min_file_size': 1,
					'accept_file_types': 'ALL',
					'max_number_of_files': None,
					'discard_aborted_uploads': True,
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
			self.options = options

	def __get_file_object(file_name):
		file_path = self.options['upload_dir'] + file_name
		if os.path.isfile(file_path) and file_name[0] != '.':
			file = Storage()
			file.name = file_name
			file.size = os.path.getsize(file_path)
			file.url = self.options['upload_url'] + \
					 urllib.urlencode(file.name)

			for version, options in self.options['image_versions']:
				if os.path.isfile(self.options['upload_dir'] + file_name):
					file[version + '_url'] = options['upload_url'] + \
										urllib.urlencode(file.name)

			file.delete_url = self.options['script_url'] + \
							"?file=" + urllib.urlencode(file.name)
			file.delete_type = 'DELETE'
			return file

		return None

	def __get_file_objects():
		files = []
		for file in os.listdir(options['upload_dir']):
			files.append(self.__get_file_object(file))
		return files

	def __create_scaled_image(file_name, options):
		# Function unimplemented because not needed by GL
		return True

	def __has_error(uploaded_file, file, error):
		if error:
			return error
		if file.split['.'][-1:][0] not in \
				self.options['accepted_file_types'] and \
				self.options['accepted_file_types'] != "ALL":
			return 'acceptFileTypes'
		if self.options['max_file_size'] and \
			(file_size > self.options['max_file_size'] or \
				file.size > self.options['max_file_size']):
			return 'maxFileSize'

		if self.options['min_file_size'] and \
			file_size > self.options['min_file_size']:
			return 'minFileSize'

		if self.options['max_number_of_files'] and \
			int(self.options['max_number_of_files']) <= \
				len(self.__get_file_objects):
			return 'maxNumberOfFiles'
		return None

	def __handle_file_upload(uploaded_file, name, size, type, error):
		file = Storage()

		file.name = os.path.basename(name).strip('.\x20\x00..')
		#file.name = strip_path_and_sanitize(name)
		file.size = int(size)
		file.type = type
		error = self.has_error(uploaded_file, file, error)

		if not error and file.name:
			file_path = self.options['upload_dir'] + file.name
			append_file = not self.options['discard_aborted_uploads'] and \
                os.path.isfile(file_path) and \
                file.size > os.path.getsize(file_path)
			if uploaded_file:
			# multipart/formdata uploads (POST method uploads)
				if append_file:
					shutil.copyfileobj(
									uploaded_file,
									open(file_path, 'ab')
									)
				else:
					shutil.copyfileobj(
									uploaded_file,
									open(file_path, 'w+b')
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
			if file_size == file.size:
				file.url = self.options['upload_url'] + \
						urllib.urlencode(file.name)

				for version, options in self.options['image_versions']:
					if os.path.isfile(self.options['upload_dir'] + file_name):
						file[version + '_url'] = options['upload_url'] + \
											urllib.urlencode(file.name)
			elif self.options['discard_aborted_uploads']:
				os.remove(file_path)
			file.error = 'abort'
			file.size = file_size
			file.delete_url = self.options['script_url'] + \
						"?file=" + urllib.urlencode(file.name)
			file.delete_type = 'DELETE'
		else:
			file.error = error

		return file

	def get():
		if request.vars.file:
			file_name = os.path.basename(request.vars.file)
			#file_name = strip_path_and_sanitize(request.vars.file)
			info = self.__get_file_object(file_name)
		else:
			filename = None
			info = self.__get_file_objects()
		return info

	def post():
		if request.vars[self.options['param_name']]:
			upload_file = request.vars[self.options['param_name']]

			upload['name'] = upload_file.filename
			upload['size'] = None
			upload['type'] = None
			upload['error'] = None
			upload['file'] = upload_file.file
			# For the moment don't handle multiple files in one POST
			if request.vars.http_x_file_name:
				info = self.__handle_file_upload(
											upload['file'],
											request.vars.http_x_file_name,
											request.vars.http_x_file_size,
											request.vars.http_x_file_type,
											upload['error']
											)
			else:
				info = self.__handle_file_upload(
											upload['file'],
											upload['name'],
											upload['size'],
											upload['type'],
											upload['error']
											)

			return info

		def delete():
			file_name = os.path.basename(request.vars.file) if request.vars.file else None
			file_path = self.options['upload_dir'] + file_name
			success = os.path.isfile(file_path) and file_name[0] != "." and os.remove(file_path)
			return success

