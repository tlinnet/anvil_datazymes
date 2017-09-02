import anvil.server

@anvil.server.callable
def exe_unittest():
  import unittest
  from unittest.case import TestCase

  from StringIO import StringIO
  
  class MyTestCase(TestCase):
      def testTrue(self):
          '''
          Always true
          '''
          assert True
  
      def testFail(self):
          '''
          Always fails
          '''
          assert False
  
  from pprint import pprint
  stream = StringIO()
  runner = unittest.TextTestRunner(stream=stream)
  result = runner.run(unittest.makeSuite(MyTestCase))
  print 'Tests run ', result.testsRun
  print 'Errors ', result.errors
  pprint(result.failures)
  stream.seek(0)
  print 'Test output\n', stream.read()