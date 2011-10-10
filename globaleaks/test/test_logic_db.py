
from globaleaks import test


from globaleaks.applications.globaleaks.modules.logic import db

import os
import os.path
# Change current working dir into a new, temporary directory
if not os.path.isdir('tmp'):
    os.mkdir('tmp')
os.chdir('tmp')

class TestDB(test.TestCase):
    """
    Varius test intended to check a new, mock database integrity.
    """

    def setUp(self):
        self.db = db.DB()

    def test_create(self):
        self.assertTrue(os.path.exists('storage.db'))
        self.assertNotEqual(self.db.tables, [])

        self.assertIn('desc', self.db.leak)
        self.assertIn('name', self.db.targetgroup)
        self.assertIn('target', self.db.tables)
        self.assertIn('comment', self.db.tables)

    def __del__(self):
        os.rmdir('tmp')

if __name__ == '__main__':
    test.main()

