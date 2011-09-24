from applications.globaleaks import test

class TestFoo(test.TestCase):
    def setUp(self):
        self.s = "foobarbaz"

    def test_foo(self):
        self.assertTrue(self.s.startswith('foo'))

if __name__ == '__main__':
    testmain()
