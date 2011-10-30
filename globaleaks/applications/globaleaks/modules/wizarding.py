from __future__ import with_statement

from xml.dom.minidom import parse, parseString
from pprint import pprint

from gluon import SQLFORM, Field
from gluon import *
from gluon import BUTTON
T = TR
BUTTON = BUTTON


class ExtraField:
    def __init__(self, filename):
        with open(filename) as xmlfile:
            self.dom = parse(xmlfile)

        self.wizard = bool(self.dom.getElementsByTagName('wizard'))
        self.fields = [self.parse_field(x) for x in
                       self.dom.getElementsByTagName('field')]


    def parse_list(self, field):
        return [x.childNodes[0].data for x in field.getElementsByTagName("el")]

    def get_content(self, field, tag):
        return field.getElementsByTagName(tag)[0].childNodes[0].data

    def parse_field(self, field):
        parsed = dict(name = self.get_content(field, "name"),
                      label = self.get_content(field, "label"),
                      desc  = self.get_content(field, "description"),
                      type  = self.get_content(field, "type"))

        if parsed['type'] == "list":
            parsed['list'] = self.parse_list(field)

        return parsed

    def __getitem__(self, k):
        return k.getAttributeNode("number").value

    def get_step_n(self, steps, n):
        for step in steps:
            if self[step] == n:
                return step
        return None

    def parse_step(self, step):
        """
        Return a list of steps parsing each step's node.
        """
        fields = ('field', 'material', 'grouplist',
                  'captcha', 'disclaimer')
        nodes = filter(lambda node: node.nodeName in fields, step.childNodes)
        return [self.parse_field(node) if node.nodeName == 'field' else
                node.nodeName
                for node in nodes]


    def gen_wizard(self):
        steps = self.dom.getElementsByTagName("step")

        wizard = []

        for i in range(0, len(steps)):
            nstep = self.get_step_n(steps, i+1)
            if nstep:
                wizard.append(self.parse_step(nstep))
            else:
                wizard.append(self.parse_step(steps[i]))

        return wizard

    def gen_db(self):
        if self.fields:
            output = []
            for i in self.fields:
                if i['type'] == "list":
                    output.append(Field(str(i['name']),requires=IS_IN_SET(i['list'])))
                    #output.append((str(i['name']), i['list']))
                else:
                    output.append(Field(str(i['name']), str(i['type'])))
                    #output.append((str(i['name']), str(i['type'])))
            return output


class FormShaman(SQLFORM):
    def __init__(self, gl, settings, *args, **kwargs):

        # XXX: shit happens
        self.gl = gl
        self.settings = settings

        # Creating a list of targetgroups
        groups_data = self.gl.get_targetgroups()
        grouplist = UL(_id="group_list")
        for group_id in groups_data:
            group = groups_data[group_id]['data']
            grouplist.insert(-1, LI(INPUT(_type="checkbox", _value="on",
                                          _name="target_%d" % group_id),
                                    SPAN(T(group["name"])),
                                    SPAN(T(group["tags"]),
                                         _class="group_tags")))

        jQueryFileUpload = DIV(
                           DIV(LABEL("Material:"),
                                _class="w2p_fl"),
                           DIV(DIV(LABEL(SPAN(T("Add Files")),
                                         INPUT(_type="file",
                                               _name="files[]"),
                                               _class="fileinput-button"),
                                   BUTTON(T("Start upload"),
                                            _type="submit",
                                            _class="start"),
                                   BUTTON(T("Cancel upload"),
                                            _type="reset",
                                            _class="cancel"),
                                   BUTTON(T("Delete Files"),
                                            _type="button",
                                            _class="delete"),
                                   _class="fileupload-buttonbar"),
                                   DIV(TABLE(_class="files"),
                                       DIV(_class="fileupload-progressbar"),
                                       _class="fileupload-content"),
                                   _id="fileupload", _class="w2p_fl"),
                            DIV(_class="w2p_fc"),
                                _id="material__row")

        material_njs = DIV(DIV(LABEL("Material:"),
                                _class="w2p_fl"),
                            DIV(INPUT(_name='material', _type='file',
                                      _id='file-uploader-nonjs'),
                                _class="w2p_fc"),
                                _id="file-uploader-nonjs")

        targetgroups = DIV('Targets', DIV(DIV(_id="group_filter"),
                                         DIV(grouplist)))


        disclaimer = DIV(LABEL('Accept Disclaimer'), self.settings.globals.disclaimer,
                         INPUT(_name='agree', value=True, _type='checkbox'))


        self.special_fields = {
                       'disclaimer' : disclaimer,#settings.globals.disclaimer_html,
                       'captcha' : '' ,#auth.settings.captcha,
                       'material': DIV(jQueryFileUpload, material_njs),#DIV(settings.globals.material_njs, settings.globals.jQueryFileUpload),
                       'grouplist': ''
                       }

        self.steps = kwargs.get('steps', None)
        if not self.steps:
            raise ValueError('FormShaman needs a steps argument')
        fields = []
        labels = []
        for step in self.steps:
            for norm_field in filter(lambda x: x not in self.special_fields.keys(),
                                     step):
                fields.append(norm_field['name'])
                labels.append({ norm_field['name'] :
                                norm_field['label'] })

        # set up everything launching the parent class' init
        super(FormShaman, self).__init__(*args, fields=fields, labels=labels, **kwargs)

    def createform(self, xfields):

        table = DIV(_id="wizard", _class="swMain")
        step_head = UL()
        for i in range(1,len(self.steps)+1):
            # XXX Make this part much more customizable, such as the stepDesc
            step_head.append(LI(
                                A(
                                  LABEL(str(i),_class="stepNumber"),
                                  SPAN("Step "+str(i),_class="stepDesc"),
                                  _href="#step-"+str(i)),
                                )
                             )
        table.append(step_head)

        try:
            i = 1
            j = 0
            for step in self.steps:
                step_html = DIV(_id="step-"+str(i))
                for field in step:
                    if field in self.special_fields.keys():
                        step_html.append(self.special_fields[field])
                    else:
                        step_html.append(DIV(xfields[j][1],xfields[j][2],_id=xfields[j][0]))
                        j += 1

                table.append(step_html)
                i += 1

        except:
            raise RuntimeError, 'formstyle not supported'

        #response.files.append(URL('static','FormShaman',args=['css','smart_wizard.css']))
        #response.files.append(URL('static','FormShaman',args=['js','jquery.smartWizard.js']))

        return table
