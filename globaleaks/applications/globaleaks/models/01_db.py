"""
Define the main globaleaks database structure.
"""

db = DAL(settings.database.uri)


db.define_table('target',
    Field('name'),
    Field('hidden', writable=False, readable=False),
    Field('desc'),
    Field('contact_type', writable=False, readable=False), 
                            # this in the future need to be the trigger of external module loading
                            # with external database loading (e.g.: gpg key, ssh key, notification and
                            # material delivery treat and configured separately, etc).
    Field('contact'),
    Field('type', writable=False, readable=False),
    # security supports - configurable by Bouquet page
    Field('password'),
    Field('password_enabled', 'boolean'),
    Field('pgpkey'),
    Field('pgpkey_enabled', 'boolean'),
    # end of security supports
    Field('info'),
    Field('candelete', writable=False),     
                            # remove capability: the capability of a receiver could be managed with a
                            # bitmask, like contact_type in the future need to be. during the development
                            # other capability might be request, could be useful provide here a flexible
                            # interface
    Field('last_sent_tulip', writable=False),
    Field('last_access', writable=False),
    Field('last_download', writable=False),
    Field('tulip_counter', writable=False),
    Field('download_counter', writable=False),
    Field('download_counter', writable=False),
    format='%(name)s'
    )

# The table for target groups
db.define_table('targetgroup',
    Field('name', unique=True),
    Field('desc'),
    Field('tags'),
    Field('targets'),
    format='%(name)s'
    )

# XXX
# Merge with submission, all references of the term "leak"
# should be removed and replaced with submission
from xml.dom.minidom import parse, parseString
from pprint import pprint

class ExtraField:
    def __init__(self, filename):
        from xml.dom.minidom import parse, parseString
        from pprint import pprint

        file = open(filename)
        dom = parse(file)
        self.dom = dom
        self.wizard = False

        self.step_desc = []
        self.fields = []

        if dom.getElementsByTagName("wizard"):
            self.wizard = True

        for i in dom.getElementsByTagName("field"):
            self.fields.append(self.parse_field(i))

    def get_content(self, field, tag):
        return field.getElementsByTagName(tag)[0].childNodes[0].data

    def parse_list(self, field):
        list = []
        for el in field.getElementsByTagName("el"):
            list.append(el.childNodes[0].data)
        return list

    def parse_field(self, field):
        parsed = {}
        parsed['name'] = self.get_content(field, "name")
        parsed['label'] = self.get_content(field, "label")
        parsed['desc']  = self.get_content(field, "description")
        parsed['type']  = self.get_content(field, "type")
        if parsed['type'] == "list":
            parsed['list'] = self.parse_list(field)
        return parsed

    def get_step(self, el):
        return el.getAttributeNode("number").value

    def get_step_n(self, steps, n):
        for step in steps:
            if self.get_step(step) == n:
                return step
        return None

    def parse_step(self, step):
        steps = []

        for node in step.childNodes:
            if node.nodeName == "field":
                steps.append(self.parse_field(node))
            elif node.nodeName == "material":
                steps.append("material")
            elif node.nodeName == "grouplist":
                steps.append("grouplist")
            elif node.nodeName == "disclaimer":
                steps.append("disclaimer")
            elif node.nodeName == "disclaimer_info":
                steps.append("disclaimer_info")
            elif node.nodeName == "captcha":
                steps.append("captcha")
            elif node.nodeName == "p":
                self.step_desc.append(node.childNodes[0].data)

        return steps

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

#extrafile = os.path.join(os.path.dirname(__file__), 'extrafields_wizard.xml')
extrafile = os.path.join(request.folder, "../../", settings.globals.extrafields_wizard)
extrafields = ExtraField(extrafile)
settings.extrafields = extrafields

db_extrafields = extrafields.gen_db()

db.define_table('leak',
    Field('title', requires=IS_NOT_EMPTY()),
    Field('desc', 'text', requires=IS_NOT_EMPTY()),
    Field('submission_timestamp'),
    Field('leaker_id', db.target),
    Field('whistleblower_access'),
    Field('notified_groups'),
    Field('spooled', 'boolean', False),
    *db_extrafields,
    format='%(name)s'
)

db.define_table('comment',
    Field('leak_id', db.leak),
    Field('commenter_name'),
    Field('commenter_id'),
    Field('comment'),
    format='%(name)s'
)

db.define_table('material',
    Field('url'), #, unique=True),
    Field('leak_id', db.leak),
    Field('type'),
    Field('async_id'),
    Field('description'),
    Field('details'),
    Field('file'),
    format='%(name)s'
)

db.define_table('tulip',
    Field('url', unique=True),
    Field('leak_id', db.leak),
    Field('target_id'),
    Field('feedbacks_provided'),
    Field('allowed_accesses'),
    Field('accesses_counter'),
    Field('allowed_downloads'),
    Field('downloads_counter'),
    Field('expiry_time'),
    format='%(name)s'
    )

# XXX
# Probably there is a better solution for spooling email
db.define_table('mail',
    Field('target'),
    Field('address'),
    Field('tulip', unique=True),
    format='%(name)s'
)

# XXX
# Merge this with leak
db.define_table('submission',
    Field('session', unique=True),
    Field('leak_id'),
    Field('dirname'),
    format='%(name)s'
)

# XXX
# This should be merged with the above
# Notification table to keep track of notifications to be sent to targets.
db.define_table('notification',
                Field('target'),
                Field('address'),
                Field('tulip'),
                Field('leak_id'),
                Field('type'),
                format='%(name)s'
)

