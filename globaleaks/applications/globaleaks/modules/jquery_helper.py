def upload_tmpl():
    return """<tr class="template-upload{{if error}} ui-state-error{{/if}}">
        <td class="preview"></td>
        <td class="name">${name}</td>
        <td class="size">${sizef}</td>
        {{if error}}
            <td class="error" colspan="2">Error:
                {{if error === 'maxFileSize'}}File is too big
                {{else error === 'minFileSize'}}File is too small
                {{else error === 'acceptFileTypes'}}Filetype not allowed
                {{else error === 'maxNumberOfFiles'}}Max number of files exceeded
                {{else}}${error}
                {{/if}}
            </td>
        {{else}}
            <td class="progress"><div></div></td>
            <td class="start"><button>Start</button></td>
        {{/if}}
        <td class="cancel"><button>Cancel</button></td>
    </tr>
    """

def download_tmpl():
    return """<tr class="template-download{{if error}} ui-state-error{{/if}}">
        {{if error}}
            <td></td>
            <td class="name">${name}</td>
            <td class="size">${sizef}</td>
            <td class="error" colspan="2">Error:
                {{if error === 1}}File exceeds upload_max_filesize (php.ini directive)
                {{else error === 2}}File exceeds MAX_FILE_SIZE (HTML form directive)
                {{else error === 3}}File was only partially uploaded
                {{else error === 4}}No File was uploaded
                {{else error === 5}}Missing a temporary folder
                {{else error === 6}}Failed to write file to disk
                {{else error === 7}}File upload stopped by extension
                {{else error === 'maxFileSize'}}File is too big
                {{else error === 'minFileSize'}}File is too small
                {{else error === 'acceptFileTypes'}}Filetype not allowed
                {{else error === 'maxNumberOfFiles'}}Max number of files exceeded
                {{else error === 'uploadedBytes'}}Uploaded bytes exceed file size
                {{else error === 'emptyResult'}}Empty file upload result
                {{else}}${error}
                {{/if}}
            </td>
        {{else}}
            <td class="preview">
                {{if thumbnail_url}}
                    <a href="${url}" target="_blank"><img src="${thumbnail_url}"></a>
                {{/if}}
            </td>
            <td class="name">
                <a href="${url}"{{if thumbnail_url}} target="_blank"{{/if}}>${name}</a>
            </td>
            <td class="size">${sizef}</td>
            <td colspan="2"></td>
        {{/if}}
        <td class="delete">
            <button data-type="${delete_type}" data-url="${delete_url}">Delete</button>
        </td>
    </tr>
    """ 

#
#def upload_tmpl():
#    return """<tr class="template-upload{{if error}} ui-state-error{{/if}}">
#            <td class="preview"></td>
#            <td class="name">${name}</td>
#            <td class="size">${sizef}</td>
#            {{if error}}
#                <td class="error" colspan="2">Error:
#                    {{if error === 'maxFileSize'}}""" + T("File is too big") + \
#                    """{{else error === 'minFileSize'}}""" + T("File is too small") + \
#                    """{{else error === 'acceptFileTypes'}}""" + T("Filetype not allowed") + \
#                    """{{else error === 'maxNumberOfFiles'}}""" + T("Max number of files exceeded") + \
#                    """{{else}}${error}
#                    {{/if}}
#                </td>
#            {{else}}
#                <td class="progress"><div></div></td>
#                <td class="start"><button>""" + T("Start") + """</button></td>
#            {{/if}}
#            <td class="cancel"><button>""" + T("Cancel") + """</button></td>
#        </tr>"""
#
#def download_tmpl():
#    return """
#        <tr class="template-download{{if error}} ui-state-error{{/if}}">
#        {{if error}}
#            <td></td>
#            <td class="name">${name}</td>
#            <td class="size">${sizef}</td>
#            <td class="error" colspan="2">Error:
#                {{if error === 1}}""" + T("File exceeds upload_max_filesize (php.ini directive)") + \
#                """{{else error === 2}}""" + T("File exceeds MAX_FILE_SIZE (HTML form directive)") + \
#                """{{else error === 3}}""" + T("File was only partially uploaded") + \
#                """{{else error === 4}}""" + T("No File was uploaded") + \
#                """{{else error === 5}}""" + T("Missing a temporary folder") + \
#                """{{else error === 6}}""" + T("Failed to write file to disk") + \
#                """{{else error === 7}}""" + T("File upload stopped by extension") + \
#                """{{else error === 'maxFileSize'}}""" + T("File is too big") + \
#                """{{else error === 'minFileSize'}}""" + T("File is too small") + \
#                """{{else error === 'acceptFileTypes'}}""" + T("Filetype not allowed") + \
#                """{{else error === 'maxNumberOfFiles'}}""" + T("Max number of files exceeded") + \
#                """{{else error === 'uploadedBytes'}}""" + T("Uploaded bytes exceed file size") + \
#                """{{else error === 'emptyResult'}}""" + T("Empty file upload result") + \
#                """{{else}}${error}
#                {{/if}}
#            </td>
#        {{else}}
#            <td class="preview">
#                {{if thumbnail_url}}
#                    <a href="${url}" target="_blank"><img src="${thumbnail_url}"></a>
#                {{/if}}
#            </td>
#            <td class="name">
#                <a href="${url}"{{if thumbnail_url}} target="_blank"{{/if}}>${name}</a>
#            </td>
#            <td class="size">${sizef}</td>
#            <td colspan="2"></td>
#        {{/if}}
#        <td class="delete">
#            <button data-type="${delete_type}" data-url="${delete_url}">""" + T("Delete") + """</button>
#        </td>
#    </tr>
#    """