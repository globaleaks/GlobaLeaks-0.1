###############################################
# Parse the extra fields.
###############################################
#!/usr/bin/env python
class ExtraField:
    def __init__(self, filename):
        from xml.dom.minidom import parse, parseString
        from pprint import pprint

        file = open(filename)
        dom = parse(file)

        self.fields = []

        for i in dom.getElementsByTagName("field"):
            self.fields.append(self.parse_field(i))


    def get_content(self, field, tag):
        return field.getElementsByTagName(tag)[0].childNodes[0].data

    def parse_list(self, field):
        list = []
        for el in  field.getElementsByTagName("el"):
            list.append(str(el.childNodes[0].data))
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
    def gen_db(self):
        if self.fields:
            output = []
            for i in self.fields:
                if i['type'] == "list":
                    output.append(Field(str(i['name']),requires=IS_IN_SET(i['list'])))
                else:
                    output.append(Field(str(i['name']), str(i['type'])))
            return output

extrafile = os.path.join(os.path.dirname(__file__), 'extrafields.xml')
extrafields = ExtraField(extrafile)
settings.extrafields = extrafields

db_extrafields = extrafields.gen_db()

################################################
# Define the main globaleaks database structure
################################################

db = DAL(settings.database.uri)

db.define_table('target',
    Field('name'),
    Field('hidden'),
    Field('desc'),
    Field('url'),
    Field('type'),
    Field('info'),
    Field('status'),
    Field('last_sent_tulip'),
    Field('last_access'),
    Field('last_download'),
    Field('tulip_counter'),
    Field('download_counter'),
    Field('groups'),
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
db.define_table('leak',
    Field('title'),
    Field('desc', 'text'),
    Field('submission_timestamp'),
    Field('leaker_id', db.target),
    Field('whistleblower_access'),
    Field('spooled', 'boolean', False),
    *db_extrafields,
    format='%(name)s'
)

db.define_table('comment',
    Field('leak_id', db.leak),
    Field('commenter_id', db.target),
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
    Field('express_vote'),
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
