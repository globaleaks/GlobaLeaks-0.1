from gluon import *

class FormShaman(SQLFORM):
    def __init__(
        self,
        table,
        record = None,
        deletable = False,
        linkto = None,
        upload = None,
        fields = None,
        labels = None,
        col3 = {},
        submit_button = 'Submit',
        delete_label = 'Check to delete:',
        showid = True,
        readonly = False,
        comments = True,
        keepopts = [],
        ignore_rw = False,
        record_id = None,
        formstyle = 'table3cols',
        buttons = ['submit'],
        separator = ': ',
        **attributes
        ):
        
        # Special fields to be replaced with custom HTML
        
        disclaimer = DIV(settings.globals.disclaimer,
                         LABEL('Accept Disclaimer:'),
                         INPUT(_name='agree', value=True, _type='checkbox')
                         )
        
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

        
        self.special_fields = {
                               'disclaimer' : disclaimer,
                               'captcha' : auth.settings.captcha,
                               'material': DIV(material_njs, jQueryFileUpload),
                               'grouplist': ''
                               }
        
        from gluon import current
        super(SQLFORM, self).__init__(
                                    table,
                                    record = None,
                                    deletable = False,
                                    linkto = None,
                                    upload = None,
                                    fields = None,
                                    labels = None,
                                    col3 = {},
                                    submit_button = 'Submit',
                                    delete_label = 'Check to delete:',
                                    showid = True,
                                    readonly = False,
                                    comments = True,
                                    keepopts = [],
                                    ignore_rw = False,
                                    record_id = None,
                                    formstyle = 'table3cols',
                                    buttons = ['submit'],
                                    separator = ': ',
                                    **attributes
                                    )

        # Check if the number of step descriptions are the same as the fields
        if len(steps) == len(fields):
            self.p_steps = steps # [{'title': 'Step 1', 'desc': 'Step 1 description'}, {'title': 'Step 2', 'desc': 'Step 2 description'}]
        else:
            return False
        
        # [{'title':'Step Title', 'fields':['fieldname1','fieldname2']}]
        self.p_tablename = form.table._tablename
        self.p_attributes = form.attributes
        self.p_elements = [e.parent for e in form.elements('.w2p_fw')]
       
        self.splitted_steps = self.split_steps()
       
        # TODO: IMPROVE IT REMOVING ALL CODE ABOVE, DOING IT INSIDE THE FORM BELOW
        FORM.__init__(self, _id=self._id ,*self.splitted_steps, **attributes)


        response.files.append(URL('static','FormShaman',args=['css','smart_wizard.css']))
        response.files.append(URL('static','FormShaman',args=['js','jquery.smartWizard.js'])) 
        
        self.append_js()       

    def __make_fields(self, step):
        for field in step:
            {'desc': 
                u'this is the main title of the submission', 
                'type': u'string', 
                'name': u'title', 
                'label': u'title'
                }, 

            if field not in self.special_fields:
                
                                
            else:
                totalfields.append(y)


    def make_steps(self):
        """
        This is how a parsed fieldset looks like:
        self.fields = 
        [
            [
                {'desc': 
                u'this is the main title of the submission', 
                'type': u'string', 
                'name': u'title', 
                'label': u'title'
                }, 
                
                {'desc': 
                    u'Describe your submission in this box', 
                'type': u'text', 
                'name': u'desc', 
                'label': u'Description'
                }, 
                
                'grouplist'
            ], 
            
            [
                'material', 
                
                {'desc': u'This is a text field', 'type': u'string', 'name': u'extratext', 'label': u'Text'}
            ], 
            
            [
                {'desc': u'Enter a date realted to your submission', 'type': u'date', 'name': u'date', 'label': u'Date'}, 
                
                'disclaimer', 
                
                'captcha'
            ]
            
        ]
        
        """

        totalfields = []
        tovalidatefields = []
        step_number = 1
        #totalfields = self.fields[:]
        for step in self.fields[:]:
            wizard_steps = DIV(self.__make_fields(step), _id="step-"+step_number)
            step_number += 1

        splitted_steps = []

        if self.options.get('validate'):
            self.fields_for_validation = tovalidatefields[:] #totalfields[:]

        while totalfields:        
            for step in self.p_steps:
                index = self.p_steps.index(step)+1
                fieldset = FIELDSET(_title=step.get('title', self.T('Step %s' % index )))
                
                if step.get('legend',None):
                    fieldset.append(LEGEND(step['legend']))

                for field in step['fields']:
                    self.indexes.append((field,index))
                    for e in self.p_elements:
                       
                        splitted_field = e.attributes['_id'].split('_')
                        
                        if len(splitted_field) == 4: 
                            p_id = splitted_field[1]
                            if field == p_id:
                                fieldset.append(e)
                        else:
                            import re
                            p_search = field + "__row"
                            if re.search(p_search, e.attributes['_id']):
                                fieldset.append(e)
    
                    if field in totalfields:
                        totalfields.remove(field)
                
                if len(fieldset.elements()) > 1: 
                    splitted_steps.append(fieldset)
        
        splitted_steps.append(INPUT(_type='submit', _class="finish", _value=self.attributes.get('submit_button','submit')))
        return splitted_steps


    def append_js(self):
        
        # Callbacks receives 'index' as argument, index is the number of the next step
        options = {
                    'back': self.options.get('back',''),                               # JS Callback before the backward action.
                    'backLabel': self.options.get('backLabel',str(self.T('< Back'))),  # Change the back button label.
                    'block': self.options.get('block', True),                          # **Block the next step if the current is invalid
                    'description': self.options.get('description',False),              # Choose if the description of the titles willbeshowed
                    'errorImage': self.options.get('errorImage',True),                 # ** If an error, shows an image at teh step title
                    'finish': self.options.get('finish', ''),                          # JS Callback before finish
                    'finishButton': self.options.get('finishButton', True),            # Include or not the button submit at the end
                    'nextLabel': self.options.get('nextLabel',str(self.T('Next >'))),  # Change the label of Next button
                    'legend': self.options.get('legend', False),                       # Choose if the legends will be showed
                    'next': self.options.get('next', ''),                              # JS Callback for next button
                    'titleClick':self.options.get('titleClick', True),                 # Active the action for title click
                    'titleTarget': self.options.get('titleTarget',''),                 # Choose the place qhere title will appear
                    'validate': self.options.get('validate', False),                   # Activate client side validations
                  }

        
        if options.get('validate'):
            insert_fields = dict(zip(self.fields, ['' for f in self.fields]))
            error_messages = self.table._db[self.table]._validate(**insert_fields)
            
            rules = {}
            messages = {}
            for k, v in error_messages.items():
                rules[k] = 'required'
                messages[k] =  str(v)     

            validatejs = """$('#%(_id)s').validate({
                        errorElement: "div",
                        errorPlacement: function(error, element){
                          //element.parent().next().html("<div style='display: block;'></div>");
                          error.prependTo(element.parent().next());  
                        },
                        rules: %(rules)s,
                        messages: %(messages)s
                    });""" % dict(_id=self._id, rules=rules, messages=messages)
        else:
            validatejs = ""

        script = """
                 $(function() {
                    $('#%(_id)s').stepy(%(options)s);
                    %(validatejs)s   
                             })""" % dict(options=str(options).replace('True','true').replace('False','false').replace('None','null'),
                                          validatejs=validatejs,
                                          _id=self._id)

        clean_script = script.replace("'back'","back").\
                              replace("'next'","next").\
                              replace("'finish'","finish").\
                              replace('"function(',"function(").\
                              replace(';}"',";}")
        self.append(SCRIPT(clean_script))

    
    def step_validation(self):
        step = None
       
        for field,index in self.indexes:
            if not step:
                if self.errors.get(field, None):
                    step = index
                    
                      
        script = """$(function() {
                     $.fn.stepy.step(%(step)s, '#%(_id)s');
                     $('.finish').show();
                             })""" % dict(step=step, _id=self._id)
                             
        self.append(SCRIPT(script))

    def validate(self, 
                values=None,
                session=None, 
                formname='default',
                keepvalues=False,
                onvalidation=None,
                hideerror=False,
                after='flash', 
                messages=[], 
                args=[]):
        """
        This function auto_validates the form, you can use it instead of directly form.accepts.

        Usage:
        In controller

        def action():
            form=FORM(INPUT(_name=\"test\", requires=IS_NOT_EMPTY()))
            form.validate()
            return dict(form=form)

        This can receive a bunch of arguments        

        after = 'flash' - will show *messages in response.flash #default
                 a function instance i.e: my_function "whithout the ()" 
                     will execute a function (first arg is always True for success and False for error)
                 None - Will perform nothing

        values = values to test the validation - dictionary, response.vars, session or other - Default to (request.vars, session)
        messages = ['success message for flash','error message for flash']
        args = list of args to be passed to function passes as after argument
        
        This method returns True on Success, False on error
        if after=function returns the function's return

        works only in 1.97.1+

        """
        from gluon import current
        if not session: session = current.session
        if not values: values = current.request.vars 
        
        success = messages[0] if (after=='flash' and messages) else self.T("Success!")
        fail = messages[1] if (after=='flash' and messages) else self.T("Errors in form, please check it out.")

        def execute_after(is_valid=False, after=after, *args):
            em = "Error in function" # Exceptions would break the form
            if args:
                try:
                    return after(is_valid, *args)
                except:
                    current.response.flash = em
            else:
                try:
                    return after(is_valid)
                except:
                    current.response.flash = em
            return is_valid 

        if self.accepts(values, session):
            if after == 'flash':
                current.response.flash = success
            elif callable(after):
                return execute_after(True, after, *args)
            return True
        elif self.errors:
            if after == 'flash':
                current.response.flash = fail
            elif callable(after):
                return execute_after(False, after, *args)
            return False 


    def process(self, values=None, session=None, **args):
        """
        Perform the .validate() method but returns the form

        Usage in controllers:
        # directly on return
        def action():
            #some code here
            return dict(form=FORM(...).process(...))

        You can use it with FORM, SQLFORM or FORM based plugins

        Examples:
        #response.flash messages
        def action():
            form = SQLFORM(db.table).process(messages=['Sucess!','Errors'])
            retutn dict(form=form)

        # callback function
        # callback receives True or False as first arg, and a list of args.
        def my_callback(status, msg):
           response.flash = "Success! "+msg if status else "Errors occured"

        # after argument can be 'flash' to response.flash messages
        # or a function name to use as callback or None to do nothing.
        def action():
            return dict(form=SQLFORM(db.table).process(after=my_callback, args=['msg']))
        """
        self.validate(values=values, session=session, **args)
        return self

    # backwards compatibility
    auto_validation = validate
            