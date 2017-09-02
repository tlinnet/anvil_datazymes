from anvil import FileMedia, BlobMedia
import anvil.server
import unittest
import random
import string

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

    # Create csv file
    self.csv_xy_in_bytes = ''
    self.csv_xy_in_bytes += 'x,y' + "\n"
    self.csv_xy_in_bytes += '2.34,3.4' + "\n"
    self.csv_xy_in_bytes += '2.12,5.6' + "\n"
    self.csv_xy_bm = BlobMedia(self.str_in_content_type, self.csv_xy_in_bytes, name=self.str_in_name)    

  def setUpCreateCsvFile(self):
    # Make random file name
    N = 12
    random_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
    str_in_content_type = "text/plain"
    str_in_name = "%s.txt" % random_string
    # Create x,y header
    csv_xy_in_bytes = ''
    csv_xy_in_bytes += 'x,y' + "\n"
    for i in range(2):
      x = float(str(random.uniform(0.0, 9.9))[0:4])
      y = float(str(random.uniform(0.0, 9.9))[0:4])
      csv_xy_in_bytes += '%s,%s'%(x, y) + "\n"

    bm = BlobMedia(str_in_content_type, csv_xy_in_bytes, name=str_in_name)
    return bm  
  
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
    # Get media
    m = self.csv_bm
    # Get header and data
    header, data = anvil.server.call('read_csv', in_bytes=m.get_bytes())
    # Get the rest
    self.assertEqual(header, ['Year', 'Make', 'Model', 'Length'])
    self.assertEqual(data, [['1997', 'Ford', 'E350', '2.34'], ['2000', 'Mercury', 'Cougar', '2.38']])

  def test_8_csv_xy_read(self):
    # Get media
    m = self.csv_xy_bm
    # Get header and data
    header, data = anvil.server.call('read_csv', in_bytes=m.get_bytes())
    # Get the rest
    self.assertEqual(header, ['x', 'y'])
    self.assertEqual(data, [['2.34', '3.4'], ['2.12', '5.6']])

  def test_9_csv_xy_check(self):
    # Check xy data
    m = self.csv_xy_bm
    xy = anvil.server.call('check_csv_xy', in_bytes=m.get_bytes())
    self.assertEqual(xy, True)
    # Get the rest
    m = self.csv_bm
    csv = anvil.server.call('check_csv_xy', in_bytes=m.get_bytes())
    self.assertEqual(csv, False)

  def test_10_upload_file(self):
    # Create randomg files
    for i in range(1):
      bm = self.setUpCreateCsvFile()

      

# What is available in unittest this sandbox? 'TestCase' and 'main'
# https://docs.python.org/2/library/unittest.html
# unittest.main([module[, defaultTest[, argv[, testRunner[, testLoader[, exit[, verbosity[, failfast[, catchbreak[, buffer]]]]]]]]]])

# 0 (quiet): you just get the total numbers of tests executed and the global result
# 1 (default): you get the same plus a dot for every successful test or a F for every failure
# 2 (verbose): you get the help string of every test and the result
unittest.main(verbosity=1)