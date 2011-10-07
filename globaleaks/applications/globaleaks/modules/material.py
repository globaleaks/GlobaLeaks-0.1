import os

class utils(object):
    def human_size(self, size, approx=False):
        SUFFIX = {1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
                  1024: ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']}

        if size < 0:
            return False

        multiple = 1024 if approx else 1000

        for suffix in SUFFIX[multiple]:
            size /= multiple
            if size < multiple:
                return '%.1f %s' % (size, suffix)

    def file_type(self, ext):
        img = ['bmp', 'gif', 'jpg', 'jpeg', 'png', 'psd',
                'pspimage', 'thm', 'tif', 'yuv', 'svg', 'ps',
                'eps', 'drw', 'ai']

        data = ['7z', 'deb','gz', 'pkg','rar','rpm','sit', 'sitx', 'gz'
                'zip', 'zipx', 'iso', 'dmg', 'toast', 'vcd']

        doc = ['doc', 'docx', 'log', 'msg', 'pages', 'rtf', 'txt',
                'wpd', 'wps', 'pdf', 'xlr', 'xls', 'csv', 'key']

        if ext in img:
            return "img"
        elif ext in doc:
            return "pdf"
        else:
            return "zip"

