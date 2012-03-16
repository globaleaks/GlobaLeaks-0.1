# Language settings
languages = settings.globals.supported_languages.split("|")
supported_languages = []
for l in languages:
    x = l.split(",")
    supported_languages.append((x[0].strip(),x[1].strip()))

# disable google translate "feature"
if T.accepted_language != session._language and 0:
    import re
    lang = re.compile('\w{2}').findall(session._language)[0]
    a = URL(r=request,c='static',f='plugin_translate/jquery.translate-1.4.3-debug-all.js')
    b = URL(r=request,c='plugin_translate',f='translate',args=lang+'.js')
    response.files.append(a)
    response.files.append(b)

def plugin_translate(languages=supported_languages):
    return [LI(A(v,
        _href="%s?_language=%s" \
            % (URL(r=request, args=request.args), v), value=session._language))
                  for v,k in languages]

    #return FORM(LI(
    #        _href="document.location='%s?_language='+jQuery(this).val()" \
    #            % URL(r=request,args=request.args),
    #        value=session._language,
    #        *[OPTION(k,_value=v) for v,k in languages]))

# Template internationalization
def localize_templates(name, lang='en'):
    fn = settings.globals.__getattr__(name).split(".")
    try:
        template_file = ".".join(fn[:-1]) + "-" + lang + "." + fn[-1]
        full_path = os.path.join(request.folder, "../../", template_file)
        if os.path.exists(full_path):
            pass
        else:
            template_file =  ".".join(fn[:-1]) + "." + fn[-1]
        settings.globals.__setattr__(name, template_file)
        fp = open(template_file, "r")
        content = fp.read()
        settings.globals.__setattr__(name + "_content", content)
    except:
        pass

for x in ["presentation_file", "disclaimer_file", "whistleblower_file", "not_anonymous_file", "extrafields_wizard"]:
    localize_templates(x, lang=session._language)
