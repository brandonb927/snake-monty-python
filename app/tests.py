import bottle, unittest
from boddle import boddle
from main import *
from api import *

class TestIt(unittest.TestCase):
  snakes = {}

  def testStart(self):
    with boddle(body='{"game":"myid"}'):
      startResponse = start()
      print 'start %s' % startResponse
      self.assertEqual(startResponse, '{"color": "red"}')

  def testMove(self):
    with boddle(body=self.generateMoveRequest1()):
      moveResponse = move()
      self.assertEqual(moveResponse, '{"move": "up"}')

  def generateMoveRequest1(self):
    moveRequest = {}
    self.addToil(moveRequest)
    self.convert(moveRequest, 
        '____________________' +
        '________2______F____' +
        '____________________' +
        '____________F_______' +
        '____________________' +
        '___F________________' +
        '____________________' +
        '____________________' +
        '____________________' +
        '__________1_________' +
        '____________________' +
        '____________________' +
        '____________________' +
        '____________F_______' +
        '____________________' +
        '____________________' +
        '________2___________' +
        '____________________' +
        '____________F_______' +
        '____________________'
    )
    moveRequest['you'] = {}
    return json.dumps(moveRequest)

  def convert(self, moveRequest, asciiPicture):
    moveRequest['board'] = {}
    moveRequest['height'] = 20
    moveRequest['width'] = 20
    moveRequest['board']['food'] = []
    moveRequest['board']['snakes'] = []
    for index in range(400):
      if asciiPicture[index] == 'F':
        moveRequest['board']['food'].append({ 'y': index /20, 'x': index % 20})
      elif asciiPicture[index] == '1':
        self.getOrCreateYou()
      elif asciiPicture[index] == '_':
        # do nothing
        print ''
      else:
        self.getOrCreateSnake(asciiPicture[index])['body'].append({ 'x': -1, 'y': -1})    
    print '%s' % json.dumps(moveRequest)

  def getOrCreateSnake(self, id):
    print self.snakes

  def addToil(self, moveRequest):
    moveRequest['game'] = { 'id': 'game1'}
    moveRequest['turn'] = 1

if __name__=='__main__':
  unittest.main()
