import bottle, unittest
from boddle import boddle
from main import *
from api import *

class TestIt(unittest.TestCase):
  def testInitial(self):
    with boddle(body='{"game":"myid"}'):
      startResponse = start()
      print 'hello string %s' % startResponse
      self.assertEqual(startResponse, '{"color": "red"}')


if __name__=='__main__':
  unittest.main()
