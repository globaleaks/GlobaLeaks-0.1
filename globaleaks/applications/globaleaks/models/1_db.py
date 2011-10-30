"""
Define the main globaleaks database structure.
"""

db = DAL(settings.database.uri)

db.define_table('target',
    Field('name'),
    Field('hidden'),
    Field('desc'),
    Field('contact_type'), # this in the future need to be the trigger of external module loading
                           # with external database loading (e.g.: gpg key, ssh key, notification and
                           # material delivery treat and configured separately, etc).
    Field('contact'),
    Field('hashpass'),
    Field('type'),
    Field('info'),
    Field('status'),
    Field('delete_cap'),    # delete capability: the capability of a receiver could be managed with a
                            # bitmask, like contact_type in the future need to be. during the development
                            # other capability might be request, could be useful provide here a flexible
                            # interface
    Field('last_sent_tulip'),
    Field('last_access'),
    Field('last_download'),
    Field('tulip_counter'),
    Field('download_counter'),
    # Field('groups'), # not used except in globaleaks.py create_target ? remind to check
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
ExtraField = local_import('wizarding').ExtraField

extrafile = os.path.join(os.path.dirname(__file__), 'extrafields_wizard.xml')
extrafields = ExtraField(extrafile)
settings.extrafields = extrafields
db_extrafields = extrafields.gen_db()

db.define_table('leak',
    Field('title'),
    Field('desc', 'text'),
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
