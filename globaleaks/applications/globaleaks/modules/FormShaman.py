# coding: utf8
"""

FormShaman by GlobaLeaks (http://globaleaks.org/)

Based on PowerFormWizard Plugin for web2py by
Bruno Cezar Rocha @rochacbruno

The MIT License

Copyright (c) 2010 Washington Botelho dos Santos (stepy)
Copyright (c) 2011 Bruno Cezar Rocha (PowerFormWizard Plugin for web2py)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""
from gluon import *

class PowerFormWizard(SQLFORM):
    """
    ## Dependencies
    - web2py framework 1.97.1+
    - jquery
    - web2py_ajax (included in web2py scaffold)
    - jquery stepy plugin (included in this plugin)
    - jquery validate plugin (included in stepy plugin)
    - jquery.stepy.css (included)
    - some optional images (included)

    ## How to use:
    1 Download the plugin in http://labs.blouweb.com/plugins/powerformwizard
    2 Include the plugin in your app via web2py admin interface
    
    3 in controllers
    #################################################################################
    # controllers/default.py
    #################################################################################
    def index():
        #steps is a dict eith the keys: title, legend, fields
        mysteps = [dict(title='Passo 1', legend='First Step', fields=['name','lastname']),
                   dict(fields=['colors','picture','bio']),
                   dict(title='Passo 3', legend='Second Step',fields=['email','password'])]
        
        # import the module
        from plugin_PowerFormWizard import PowerFormWizard
        
        # create the form  
        # You can pass in any SQLFORM attibute or _html attribute          
        form = PowerFormWizard(
                               db.person,                   # A table
                               steps=mysteps,               # steps is a dictionary
                               options=dict(validate=True)  # options is a dict, in this case activate client side validation 
                               ) 
        
        # do the form validation
        if form.accepts(request.vars, session):
            response.flash = "Records inserted"
        elif form.errors:
            form.step_validation() # IMPORTANT FOR VALIDATION
            response.flash = "Errors in form, take a look"
        
        # THE FORM IS DONE, ENJOY!
        return dict(form=form) 
    
    ###################################################################################
    #  OPTIONS is a dictionary - if not passed the default is assumed
    ###################################################################################

    # Callbacks receives 'index' as argument, index is the number of the next step
    options = {
                'back': None,                       # JS Callback before the backward action.
                'backLabel': str(T('< Back'))       # Change the back button label.
                'block': True,                      # **Block the next step if the current is invalid
                'description': False,               # Choose if the description of the titles will be showed
                'errorImage': True,                 # ** If an error, shows an image at teh step title
                'finish': None,                     # JS Callback before finish
                'finishButton': True,               # Include or not the button submit at the end
                'nextLabel': str(T('Next >')),      # Change the label of Next button
                'legend': False,                    # Choose if the legends will be showed
                'next': None,                       # JS Callback for next button
                'titleClick':True,                  # Active the action for title click
                'titleTarget': '',                  # Choose the place qhere title will appear
                'validate': False,                  # Activate client side validations
              }

    ###################################################################################
    # NOTES
    ###################################################################################
    
    Client side validation is activated with options=dict(validate=True,)
    this validations is done by jquery validate and is based on db/FORM validators 
    defined in .requires


    Client side validation is not supposed to validate everything!
    Know Java Script? Wanna contribute?

    """
    
    def __init__(self, 
                 table, 
                 steps, 
                 formstyle = 'divs',
                 options={},
                 _id = 'powerformwizard',
                 record = None,
                 fields = None,
                 ignore_rw = False, 
                 record_id=None,
                 **attributes
                 ):

        if formstyle not in ['divs','ul']:
            raise AttributeError("SQLFORM formstyle not accepted")
        
        
        
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
        response = current.response
        self.T = current.T
        self.table = table
        self.formstyle = formstyle
        self.attributes = attributes
        self.ignore_rw = ignore_rw
        self.record_id = record_id
        self.options = options
        self._id = _id

        self.fields = []
        self.indexes = []
        for s in steps:
            for field in s['fields']:
                self.fields.append(field)
        
        self.record = record

        from gluon.storage import Storage   
        self.custom = Storage() # Needed to silence errors, but Custom Forms are not allowed!

        # NEEDED TO CREATE A SQLFORM OBJECT HERE TO EXTRACT DOM ELEMENTS, HOW TO DO BETTER?
        form = SQLFORM(self.table, formstyle=self.formstyle, **attributes)
        

        self.p_form = form
        self.p_steps = steps # [{'title':'Step Title', 'fields':['fieldname1','fieldname2']}]
        self.p_tablename = form.table._tablename
        self.p_attributes = form.attributes
        self.p_elements = [e.parent for e in form.elements('.w2p_fw')]
       
        self.splitted_steps = self.split_steps()
       
        # TODO: IMPROVE IT REMOVING ALL CODE ABOVE, DOING IT INSIDE THE FORM BELOW
        FORM.__init__(self, _id=self._id ,*self.splitted_steps, **attributes)


        response.files.append(URL('static','plugin_PowerFormWizard',args=['css','jquery.stepy.css']))
        response.files.append(URL('static','plugin_PowerFormWizard',args=['js','jquery.stepy.min.js'])) 
        response.files.append(URL('static','plugin_PowerFormWizard',args=['js','jquery.validate.min.js'])) 
        
        
        self.append_js()       


    def split_steps(self):
        """
        This is how a parsed fieldset looks like:
        
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
        
        For copy paste purposes, here is the one liner:
        [[{'desc': u'this is the main title of the submission', 'type': u'string', 'name': u'title', 'label': u'title'}, {'desc': u'Describe your submission in this box', 'type': u'text', 'name': u'desc', 'label': u'Description'}, 'grouplist'], ['material', {'desc': u'This is a text field', 'type': u'string', 'name': u'extratext', 'label': u'Text'}], [{'desc': u'Enter a date realted to your submission', 'type': u'date', 'name': u'date', 'label': u'Date'}, 'disclaimer', 'captcha']]
        """

        totalfields = []
        tovalidatefields = []

        #totalfields = self.fields[:]
        for x in self.fields[:]:
            for y in x:
                if y not in self.special_fields:
                    tovalidatefields.append(y['name'])
                    totalfields.append(y['name'])
                else:
                    totalfields.append(y)

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
                    'description': self.options.get('description',False),              # Choose if the description of the titles will be showed
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
            