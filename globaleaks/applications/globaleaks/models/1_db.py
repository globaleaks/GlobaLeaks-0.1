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
    Field('name'),
    Field('desc'),
    Field('tags'),
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

