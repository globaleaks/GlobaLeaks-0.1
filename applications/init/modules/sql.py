import os
import sys
from gluon.sql import DAL, Field

class DB(DAL):
    def __init__(self):
        DAL.__init__(self, 'sqlite://storage.db')
        self.create_db()
    
    def create_db(self):
        self.define_table('target',
            Field('name'),
            Field('type'),
            Field('auth_type'),
            Field('details'),
            format='%(name)s'
            )
            
        self.define_table('leak',
            Field('title'),
            Field('desc'),
            Field('submission_timestamp'),
            Field('leaker_id', self.target),
            format='%(name)s'
            )
        
        self.define_table('material',
            Field('url', unique=True),
            Field('leak_id', self.leak),
            Field('type'),
            format='%(name)s'
            )
            
        self.define_table('tulip',
            Field('uri', unique=True),
            Field('leak_id', self.leak),
            Field('target_id'),# self.target),
            Field('downloads_counter'),
            Field('allowed_downloads'),
            Field('expiry_time'),
            format='%(name)s'
            )

db = DB()

