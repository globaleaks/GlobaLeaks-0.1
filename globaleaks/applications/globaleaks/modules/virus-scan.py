###
### Submit a sample to VirusTotal and check the result.
### Based on example code by Bryce Boe, downloaded from:
### http://www.bryceboe.com/2010/09/01/submitting-binaries-to-virustotal/
###
### Needs Python 2.6 or 2.7
###
### Usage:
###  - Put your VirusTotal API key in the file virus-scan.key in the current
###    working directory (obtain from http://www.virustotal.com/advanced.html#publicapi)
###  - Run PATH/TO/PYTHON virus-scan.py FILE_TO_SCAN
###
### Copyright 2010 Steven J. Murdoch <http://www.cl.cam.ac.uk/users/sjm217/>
### See LICENSE for licensing information
###

import hashlib, httplib, mimetypes, os, pprint, json, sys, urlparse

DEFAULT_TYPE = 'application/octet-stream'

REPORT_URL = 'https://www.virustotal.com/api/get_file_report.json'
SCAN_URL = 'https://www.virustotal.com/api/scan_file.json'

API_KEY_FILE = 'virus-scan.key'

# The following function is modified from the snippet at:
# http://code.activestate.com/recipes/146306/
def encode_multipart_formdata(fields, files=()):
    """
    fields is a dictionary of name to value for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be
    uploaded as files.
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = '\r\n'
    L = []
    for key, value in fields.items():
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' %
                 (key, filename))
        content_type = mimetypes.guess_type(filename)[0] or DEFAULT_TYPE
        L.append('Content-Type: %s' % content_type)
        L.append('')
        L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body

def post_multipart(url, fields, files=()):
    """
    url is the full to send the post request to.
    fields is a dictionary of name to value for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be
    uploaded as files.
    Return body of http response.
    """
    content_type, data = encode_multipart_formdata(fields, files)
    url_parts = urlparse.urlparse(url)
    if url_parts.scheme == 'http':
        h = httplib.HTTPConnection(url_parts.netloc)
    elif url_parts.scheme == 'https':
        h = httplib.HTTPSConnection(url_parts.netloc)
    else:
        raise Exception('Unsupported URL scheme')
    path = urlparse.urlunparse(('', '') + url_parts[2:])
    h.request('POST', path, data, {'content-type':content_type})
    return h.getresponse().read()

def scan_file(filename, api_key):
    files = [('file', filename, open(filename, 'rb').read())]
    json_result = post_multipart(SCAN_URL, {'key':api_key}, files)
    return json.loads(json_result)

def get_report(filename, api_key):
    md5sum = hashlib.md5(open(filename, 'rb').read()).hexdigest()
    json_result = post_multipart(REPORT_URL, {'resource':md5sum, 'key':api_key})
    data = json.loads(json_result)
    if data['result'] != 1:
        print 'Result not found, submitting file.'
        data = scan_file(filename, api_key)
        if data['result'] == 1:
            print 'Submit successful.'
            print 'Please wait a few minutes and try again to receive report.'
            return 1
        else:
            print 'Submit failed.'
            pprint.pprint(data)
            return 1
    else:
        #pprint.pprint(data['report'])
        scan_date, result_dict = data['report']
        print "Scanned on:", scan_date

        failures = 0
        for av_name, result in result_dict.items():
            if result != '':
                failures += 1
                print " %20s: %s"%(av_name, result)
        if not failures:
            print 'SUCCESS: no AV detection triggered'
            return 0
        else:
            print 'FAIL: %s AV detection(s)'%failures
            return 255

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: %s filename' % sys.argv[0]
        sys.exit(1)

    try:
        key_fh = open(API_KEY_FILE, "rt")
        api_key = key_fh.readline().strip()
        key_fh.close()
    except IOError, e:
        print 'Failed to open API key file %s: %s' % (API_KEY_FILE, e)
        sys.exit(1)

    filename = sys.argv[1]
    if not os.path.isfile(filename):
        print '%s is not a valid file' % filename
        sys.exit(1)

    exit_status = get_report(filename, api_key)
    sys.exit(exit_status)
