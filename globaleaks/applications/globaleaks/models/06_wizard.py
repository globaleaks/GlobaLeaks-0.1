class FormShaman(SQLFORM):
    def __init__(self, *args, **kwargs):

        # Creating a list of targetgroups
        groups_data = gl.get_targetgroups()

        # unroll the effective receiver inside the groups list
        # because could exist one or more group empty!
        effective_notification = 0
        for group_id in groups_data:
            effective_notification += len(groups_data[group_id]['members'])

        # this is the only error trapped by FormShaman.__init__
        if not groups_data or not effective_notification:
            return None

        if len(groups_data) > 1:
            grouplist = UL(_id="group_list")
            for group_id in groups_data:
                group = groups_data[group_id]['data']
                grouplist.insert(-1, LI(INPUT(_type="checkbox", _value="on",
                                              _name="target_%d" % group_id),
                                        SPAN(T(group["name"])),
                                        SPAN(T(group["tags"]),
                                             _class="group_tags")))
            grouplist = DIV(LABEL(T("Select Group:"),_class="submit_label"),grouplist,_class="groups")

        else:
            grouplist = ""

        jQueryFileUpload = DIV(
                           DIV(LABEL(T("Material") + ":", _class="submit_label"),
                                _class="w2p_fl"),
                           DIV(DIV(LABEL(DIV(T("Add Files")),
                                         INPUT(_type="file",
                                               _name="files[]"),
                                               _class="fileinput-button"),
                                       DIV(SPAN(),_id="speedbox"),
#                                   BUTTON(T("Cancel upload"),
#                                            _type="reset",
#                                            _class="cancel"),
#                                   BUTTON(T("Delete Files"),
#                                            _type="button",
#                                            _class="delete"),
                                   _class="fileupload-buttonbar"),
                                   DIV(TABLE(_class="files"),
                                       DIV(_class="fileupload-progressbar"),
                                       _class="fileupload-content"),
                                   _id="fileupload", _class="w2p_fl"),
                            DIV(_class="w2p_fc"),
                                _id="material__row")

        material_njs = DIV(DIV(LABEL(T("Material") + ":", _class="submit_label"),
                                _class="w2p_fl"),
                            DIV(INPUT(_name='material', _type='file',
                                      _id='file-uploader-nonjs'),
                                _class="w2p_fc"),
                                _id="file-uploader-nonjs")

        targetgroups = DIV(T('Targets'), DIV(DIV(_id="group_filter"),
                                         DIV(grouplist)))

        with open(settings.globals.disclaimer_file) as filestream:
            disclaimer_text = TAG(filestream.read())
            # sadly, HTML must not be passed to avoid XXSs

        disclaimer_info = DIV(disclaimer_text, _class="disclaimer_text")
        disclaimer_fb = DIV(LABEL(INPUT(_name='agree', value=False, _type='checkbox',
                                        _id="disclaimer",
                                        requires=IS_EQUAL_TO("on",
                                            error_message=T('must accept disclaimer'))),T('Accept Disclaimer')),
                            INPUT(_type="submit",_id="submission-button", _class="btn"))

        self.special_fields = {
                       'disclaimer_info' : disclaimer_info,
                       'disclaimer' : disclaimer_fb,
                       'captcha' : '' ,#auth.settings.captcha,
                       'material': DIV(jQueryFileUpload, material_njs),
                       #DIV(settings.globals.material_njs, settings.globals.jQueryFileUpload),
                       'grouplist': grouplist
                       }

        self.steps = kwargs.get('steps', None)
        if not self.steps:
            raise ValueError('FormShaman needs a steps argument')
        fields = []
        labels = {}
        for step in self.steps:
            for norm_field in filter(lambda x: x not in self.special_fields.keys(),
                                     step):
                fields.append(norm_field['name'])
                labels[norm_field['name']] = norm_field['label']

        # set up everything launching the parent class' init
        super(FormShaman, self).__init__(*args, fields=fields, labels=labels, **kwargs)
        # This is a hack to make the form submission work on Chrome
        if not self['_action']:
            self['_action'] = "#"

    def createform(self, xfields):
        table = DIV(_id="submission", _class="")
        step_head = UL(_class="nav nav-tabs", _id="submission-steps")
        for i in range(1,len(self.steps)+1):
            classval = "step active" if i == 1 else "step"
            # XXX Make this part much more customizable, such as the stepDesc
            step_head.append(LI(
                                A(
                                  #SPAN(str(i),_class="stepNumber"),
                                  SPAN(T("Step") + " " +str(i),_class="stepDesc"),
                                  _href="#step-"+str(i)), _class=classval
                                )
                             )
        table.append(step_head)

        try:
            i = 1
            j = 0
            steps = []
            for step in self.steps:
                classval = "tab-pane active" if i == 1 else "tab-pane"
                step_html = DIV(FIELDSET(
                                     P(settings.extrafields.step_desc[i-1]),
                                     _id="step-"+str(i), _class="step_holder"
                                     ), _class=classval, _id="step-"+str(i))
                for field in step:
                    if field in self.special_fields.keys():
                        step_html.append(DIV(self.special_fields[field],
                                             _class="field_holder"))
                    else:
                        step_html.append(DIV(
                                             xfields[j][1],
                                             xfields[j][2],
                                             _id=xfields[j][0], _class="field_holder"))
                        j += 1
                i += 1
                steps.append(step_html)

            table.append(DIV(steps, _class="tab-content"))

        except:
            raise RuntimeError, 'formstyle not supported'

        #response.files.append(URL('static','FormShaman',args=['css','smart_wizard.css']))
        #response.files.append(URL('static','FormShaman',args=['js','jquery.smartWizard.js']))
        return table
