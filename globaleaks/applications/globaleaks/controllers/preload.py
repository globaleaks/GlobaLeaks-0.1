import os
import gluon.contenttype

from slimit import minify

def js():
    files = ['/js/jquery.js',
             '/js/modernizr-1.7.min.js',
             '/js/superfish.js',
             '/js/cufon.js',
             '/js/AlteHaas_700.font.js',
             '/js/web2py_ajax.js',
             '/js/calendar.js',
             #'/js/main.js',
             '/js/fancybox/jquery.fancybox-1.3.4.pack.js',
             '/js/fileupload/jquery-ui.min.js',
             '/FormShaman/js/jquery.smartWizard.js',
             '/js/fileupload/jquery.iframe-transport.js',
             '/js/fileupload/jquery.fileupload.js',
             '/js/fileupload/jquery.fileupload-ui.js'
             ]
    
    output_file = os.path.join(request.folder, 'static') + "/main_js_file.js"

    response.headers['Content-Type'] = gluon.contenttype.contenttype('.js')
    
    if os.path.exists(output_file):
        return response.stream(open(output_file, 'rb'))

    fh = open(output_file, 'w')
    to_minify = ""
    
    for file in files:
        path = os.path.join(request.folder, 'static') + str(file)
        for line in open(path).readlines():
            fh.write(line)
            #to_minify += line
            
    #fh.write(minify(to_minify, mangle=False))
            
    fh.close()
    
    return response.stream(open(output_file, 'rb'))
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

    response.headers['Content-Type'] = gluon.contenttype.contenttype('.css')
    
    if os.path.exists(output_file):
        return response.stream(open(output_file, 'rb'))
    
    fh = open(output_file, 'w')

    for file in files:
        path = os.path.join(request.folder, 'static') + str(file)
        for line in open(path).readlines():
            fh.write(line)

    fh.close()

    return response.stream(open(output_file, 'rb'))
