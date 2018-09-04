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
    moveRequest['board']['snakes'] = self.snakes
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
