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

class FormShaman(SQLFORM):
    def __init__(self, *args, **kwargs):
        
        self.special_fields = {
                       'disclaimer' : '',#settings.globals.disclaimer_html,
                       'captcha' : auth.settings.captcha,
                       'material': '',#DIV(settings.globals.material_njs, settings.globals.jQueryFileUpload),
                       'grouplist': ''
                       }
        
        if kwargs['steps']:
            self.steps = kwargs['steps']
            kwargs['fields'] = []
            kwargs['labels'] = []
            for step in kwargs['steps']:
                for a in step:
                    if a not in self.special_fields.keys():
                        kwargs['fields'].append(str(a['name']))
                        kwargs['labels'].append({ str(a['name']) : str(a['label']) })
        
        print kwargs['labels']
        print kwargs['fields']
        super(FormShaman, self).__init__(*args, **kwargs)
        
    
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
        #print "fields: %s " % self.fields
        
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
