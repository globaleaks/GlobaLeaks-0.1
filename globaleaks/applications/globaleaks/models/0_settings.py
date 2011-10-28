import ConfigParser
import os.path

from gluon.storage import Storage
from config import ConfigFile, cfgfile

################################################################
# Import the database and global settings from the config file #
################################################################

settings = Storage()

settings.globals = ConfigFile(cfgfile, 'global')
settings.database = ConfigFile(cfgfile, 'database')


#######
# XXX: SHIT HAPPENS
######

class FormShaman(SQLFORM):
    def __init__(self, *args, **kwargs):

        self.special_fields = {
                       'disclaimer' : '',#settings.globals.disclaimer_html,
                       'captcha' : auth.settings.captcha,
                       'material': '',#DIV(settings.globals.material_njs, settings.globals.jQueryFileUpload),
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
            for step in self.steps:
                step_html = DIV(_id="step-"+str(i))
                for field in step:
                    if field in self.special_fields.keys():
                        step_html.append(self.special_fields[field])
                    else:
                        step_html.append(DIV(xfields[i-1][1],xfields[i-1][2],_id=xfields[i-1][0]))
                table.append(step_html)
                i += 1

        except:
            raise RuntimeError, 'formstyle not supported'

        return table
