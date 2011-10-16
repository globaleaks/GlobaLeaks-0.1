import unittest

import os
import tempfile

class TestDB(unittest.TestCase):
    """
    Varius test intended to check a new, mock database integrity.
    """

    def setUp(self):
        # Change current working dir into a new, temporary directory
        dir_name = tempfile.mkdtemp()
        os.chdir(dir_name)
        self.db = db #.DB()

    def test_create(self):
        self.assertNotEqual(self.db.tables, [])

        self.assertIn('desc', self.db.leak)
        self.assertIn('name', self.db.targetgroup)
        self.assertIn('target', self.db.tables)
        self.assertIn('comment', self.db.tables)

    def __del__(self):
        os.removedirs(dir_name)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDB)
    unittest.TextTestRunner(verbosity=2).run(suite)
