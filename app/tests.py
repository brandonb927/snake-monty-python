import bottle, unittest
from boddle import boddle
from main import *
from api import *

class TestIt(unittest.TestCase):
  snakes = {}
  you = { 'id' :'1', 'body': []}

  def testStart(self):
    with boddle(body='{"game":"myid"}'):
      startResponse = start()
      print 'start %s' % startResponse
      self.assertEqual(startResponse, '{"color": "red"}')

  def testMoveInitial(self):
    with boddle(body=self.generateMoveRequest(
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
        '________3___________' +
        '____________________' +
        '____________F_______' +
        '____________________')):
      moveResponse = move()
      self.assertEqual(moveResponse, '{"move": "up"}')

  def testMoveTopWall(self):
    with boddle(body=self.generateMoveRequest(
        '___________1________' +
        '________2______F____' +
        '____________________' +
        '____________F_______' +
        '____________________' +
        '___F________________' +
        '____________________' +
        '____________________' +
        '____________________' +
        '____________________' +
        '____________________' +
        '____________________' +
        '____________________' +
        '____________F_______' +
        '____________________' +
        '____________________' +
        '________3___________' +
        '____________________' +
        '____________F_______' +
        '____________________')):
      moveResponse = move()
      self.assertEqual(moveResponse, '{"move": "right"}')

  def testMoveTopRightWall(self):
    with boddle(body=self.generateMoveRequest(
        '___________________1' +
        '________2______F____' +
        '____________________' +
        '____________F_______' +
        '____________________' +
        '___F________________' +
        '____________________' +
        '____________________' +
        '____________________' +
        '____________________' +
        '____________________' +
        '____________________' +
        '____________________' +
        '____________F_______' +
        '____________________' +
        '____________________' +
        '________3___________' +
        '____________________' +
        '____________F_______' +
        '____________________')):
      moveResponse = move()
      self.assertEqual(moveResponse, '{"move": "down"}')

  def testMoveBottomRightWall(self):
    with boddle(body=self.generateMoveRequest(
        '____________________' +
        '________2______F____' +
        '____________________' +
        '____________F_______' +
        '____________________' +
        '___F________________' +
        '____________________' +
        '____________________' +
        '____________________' +
        '____________________' +
        '____________________' +
        '____________________' +
        '____________________' +
        '____________F_______' +
        '____________________' +
        '____________________' +
        '________3___________' +
        '____________________' +
        '____________F_______' +
        '___________________1)):
      moveResponse = move(')
      self.assertEqual(moveResponse, '{"move": "left"}')

  def testMoveBottomLeftWall(self):
    with boddle(body=self.generateMoveRequest(
        '____________________' +
        '________2______F____' +
        '____________________' +
        '____________F_______' +
        '____________________' +
        '___F________________' +
        '____________________' +
        '____________________' +
        '____________________' +
        '____________________' +
        '____________________' +
        '____________________' +
        '____________________' +
        '____________F_______' +
        '____________________' +
        '____________________' +
        '________3___________' +
        '____________________' +
        '____________F_______' +
        '1___________________')):
      moveResponse = move()
      self.assertEqual(moveResponse, '{"move": "left"}')

  def testMoveTopLeftWall(self):
    with boddle(body=self.generateMoveRequest(
        '1___________________' +
        '________2______F____' +
        '____________________' +
        '____________F_______' +
        '____________________' +
        '___F________________' +
        '____________________' +
        '____________________' +
        '____________________' +
        '____________________' +
        '____________________' +
        '____________________' +
        '____________________' +
        '____________F_______' +
        '____________________' +
        '____________________' +
        '________3___________' +
        '____________________' +
        '____________F_______' +
        '____________________')):
      moveResponse = move()
      self.assertEqual(moveResponse, '{"move": "right"}')

  def generateMoveRequest(self, asciiBoard):
    moveRequest = {}
    self.addToil(moveRequest)
    self.convert(moveRequest, 
        asciiBoard
    )
    moveRequest['you'] = {}
    return json.dumps(moveRequest)

  def convert(self, moveRequest, asciiPicture):
    moveRequest['board'] = {}
    moveRequest['height'] = 20
    moveRequest['width'] = 20
    moveRequest['board']['food'] = []
    for index in range(400):
      if asciiPicture[index] == 'F':
        moveRequest['board']['food'].append({ 'y': index /20, 'x': index % 20})
      elif asciiPicture[index] == '1':
        self.you['body'].append({ 'y': index /20, 'x': index % 20})   
      elif asciiPicture[index] == '_':
        pass
      else:
        self.getOrCreateSnake(asciiPicture[index])['body'].append({ 'y': index /20, 'x': index % 20})    
    
    # help
    moveRequest['board']['snakes'] = self.snakes.values()
    moveRequest['board']['you'] = self.you
    print '%s' % json.dumps(moveRequest)

  def getOrCreateSnake(self, id):
    if id not in self.snakes:
      self.snakes[id] = { 'id': id }
      self.snakes[id]['body'] = []
    return self.snakes[id]

  def addToil(self, moveRequest):
    moveRequest['game'] = { 'id': 'game1'}
    moveRequest['turn'] = 1

if __name__=='__main__':
  unittest.main()
