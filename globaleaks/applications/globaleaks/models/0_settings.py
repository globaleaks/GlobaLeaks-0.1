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
    def __init__(self, steps, *args, **kwargs):

        self.special_fields = {
                       'disclaimer' : '',#settings.globals.disclaimer_html,
                       'captcha' : auth.settings.captcha,
                       'material': '',#DIV(settings.globals.material_njs, settings.globals.jQueryFileUpload),
                       'grouplist': ''
                       }
        print self.steps
        if steps:
            self.steps = steps
            fields = []
            labels = []
            for step in self.steps:
                for special_field in (x for x in step if x in self.special_fields):
                    fields.append(special_field['name'])
                    labels.append({ special_field['name'] :
                                    special_field['label'] })

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

        return table
