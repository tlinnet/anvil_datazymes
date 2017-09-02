from anvil import FileMedia, BlobMedia
import unittest

class TestMethods(unittest.TestCase):
  def setUp(self):
    # Create BlobMedia from string
    self.str_in_content_type = "text/plain"
    self.str_in_bytes = "Hello, world"
    self.str_in_name = "hello.txt"
    # Create BlobMedia
    self.str_bm = BlobMedia(self.str_in_content_type, self.str_in_bytes, name=self.str_in_name)

    # Create csv file
    self.csv_in_bytes = ''
    self.csv_in_bytes += 'Year,Make,Model,Length' + "\n"
    self.csv_in_bytes += '1997,Ford,E350,2.34' + "\n"
    self.csv_in_bytes += '2000,Mercury,Cougar,2.38' + "\n"
    self.csv_bm = BlobMedia(self.str_in_content_type, self.csv_in_bytes, name=self.str_in_name)

  def test_1_string_upper(self):
    # Test uppercase
    self.assertEqual('foo'.upper(), 'FOO')

  def test_2_string_isupper(self):
    # Test isupper
    self.assertTrue('FOO'.isupper())
    self.assertFalse('Foo'.isupper())

  def test_3_string_split(self):
    # Test split
    s = 'hello world'
    self.assertEqual(s.split(), ['hello', 'world'])

  def test_4_math_multiplikation(self):
    # Test math operation
    self.assertEqual(2*2, 4)

  def test_5_BlobMedia_str(self):
    # Test media properties
    m = self.str_bm
    self.assertEqual(self.str_in_content_type, m.get_content_type() )
    self.assertEqual(self.str_in_bytes, m.get_bytes() )
    self.assertEqual(self.str_in_name, m.get_name() )
    self.assertEqual(len(self.str_in_bytes), m.get_length() )

  def test_6_BlobMedia_csv(self):
    # Test creation of media
    m = self.csv_bm
    self.assertEqual(self.str_in_content_type, m.get_content_type() )
    self.assertEqual(self.csv_in_bytes, m.get_bytes() )
    self.assertEqual(self.str_in_name, m.get_name() )
    self.assertEqual(len(self.csv_in_bytes), m.get_length() )

  def test_7_csv_read(self):
    # Test creation of media
    m = self.csv_bm
    
    
# What is available in unittest this sandbox? 'TestCase' and 'main'
# https://docs.python.org/2/library/unittest.html
# unittest.main([module[, defaultTest[, argv[, testRunner[, testLoader[, exit[, verbosity[, failfast[, catchbreak[, buffer]]]]]]]]]])

# 0 (quiet): you just get the total numbers of tests executed and the global result
# 1 (default): you get the same plus a dot for every successful test or a F for every failure
# 2 (verbose): you get the help string of every test and the result
unittest.main(verbosity=1)