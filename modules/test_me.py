import unittest

class TestMe(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')