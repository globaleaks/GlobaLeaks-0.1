import os, gzip
import gluon.contenttype

def js():
    files = ['/js/jquery-1.6.4.min.js',
             '/js/modernizr-1.7.min.js',
             '/js/superfish.js',
             '/js/cufon.js',
             '/js/AlteHaas_700.font.js',
             '/js/web2py_ajax.js',
             '/js/calendar.js',
             #'/js/main.js',
             '/js/fancybox/jquery.fancybox-1.3.4.pack.js',
             '/js/fileupload/jquery-ui.min.js',
             '/js/jquery.inlineedit.js',
             '/FormShaman/js/jquery.smartWizard.js',
             '/js/fileupload/jquery.iframe-transport.js',
             '/js/fileupload/jquery.fileupload.js',
             '/js/fileupload/jquery.fileupload-ui.js',
             '/js/fileupload/jquery.tmpl.min.js',
             '/js/jquery.qtip-1.0.0-rc3.min.js',
             '/js/jquery.cookie.js'

             ]

    output_file = os.path.join(request.folder, 'static') + "/main_js_file.js"
    compressed_file = os.path.join(request.folder, 'static') + "/main_js_file.js.gz"

    response.headers['Content-Encoding'] = 'gzip'
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.js')
    response.headers['Cache-Control'] =  "max-age=86400, private"
    response.headers['Pragma'] = "cache"

    if os.path.exists(output_file):
        return response.stream(open(compressed_file, 'rb'))

    fh = open(output_file, 'wb')
    fhg = gzip.open(compressed_file, 'wb')

    to_minify = ""

    for file in files:
        path = os.path.join(request.folder, 'static') + str(file)
        for line in open(path).readlines():
            fh.write(line)
            fhg.write(line)
            #to_minify += line

    #fh.write(minify(to_minify, mangle=False))
    fhg.close()
    fh.close()

    return response.stream(open(compressed_file, 'rb'))
        #for line in open(path).readlines():
        #    output += line
    #response.stream(output)

def css():
    files = ['/css/base.css',
             '/css/superfish.css',
             '/js/fancybox/jquery.fancybox-1.3.4.css',
             '/css/calendar.css',
             #'/css/jq-fileupload.css',
             '/FormShaman/css/smart_wizard.css',
             '/css/jquery.fileupload-ui.css',
             '/css/jquery-ui.css'
             ]

    output_file = os.path.join(request.folder, 'static') + "/main_css_file.css"
    compressed_file = os.path.join(request.folder, 'static') + "/main_css_file.css.gz"

    #response.headers['Content-Encoding'] = 'gzip'
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.css')
    response.headers['Cache-Control'] =  "max-age=86400, private"
    response.headers['Pragma'] = "cache"

    #time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())

    if os.path.exists(output_file):
        return response.stream(open(output_file, 'rb'))

    fh = open(output_file, 'wb')
    #fhg = gzip.open(compressed_file, 'wb')

    for file in files:
        path = os.path.join(request.folder, 'static') + str(file)
        for line in open(path).readlines():
            fh.write(line)
            #fhb.write(line)

    #fhg.close()
    fh.close()

    return response.stream(open(output_file, 'rb'))
