import unittest

class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])

class TestMultiplikation(unittest.TestCase):
    def test_multiplikation(self):
        self.assertEqual(2*2, 4)

# What is available in unittest this sandbox? 
#print(dir(unittest))
# ['TestCase', '__author__', '__doc__', '__file__', '__name__', '__path__', 'main']

# What is available in unittest.main this sandbox? 
# https://docs.python.org/2/library/unittest.html
# unittest.main([module[, defaultTest[, argv[, testRunner[, testLoader[, exit[, verbosity[, failfast[, catchbreak[, buffer]]]]]]]]]])
test = unittest.main(verbosity=3)