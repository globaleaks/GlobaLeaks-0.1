import unittest

class TestFoo(unittest.TestCase):
    def setUp(self):
        self.s = "foobarbaz"

    def test_foo(self):
        self.assertTrue(self.s.startswith('foo'))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFoo)
    unittest.TextTestRunner(verbosity=2).run(suite)
