from anvil import FileMedia
import unittest

class TestMethods(unittest.TestCase):
    def test_string_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_string_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_string_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])

    def test_math_multiplikation(self):
        self.assertEqual(2*2, 4)

    def test_filemedia(self):
      # File 1.txt uploaded via git clone repository
      fm = FileMedia("1.txt")
      print(dir(fm))
        
# What is available in unittest this sandbox? 'TestCase' and 'main'
# https://docs.python.org/2/library/unittest.html
# unittest.main([module[, defaultTest[, argv[, testRunner[, testLoader[, exit[, verbosity[, failfast[, catchbreak[, buffer]]]]]]]]]])

# 0 (quiet): you just get the total numbers of tests executed and the global result
# 1 (default): you get the same plus a dot for every successful test or a F for every failure
# 2 (verbose): you get the help string of every test and the result
unittest.main(verbosity=1)