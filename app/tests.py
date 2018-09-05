import bottle, unittest
from boddle import boddle
from main import *
from api import *

class TestIt(unittest.TestCase):
  def setUp(self):
    print "----- In method %s -----" % self._testMethodName
    self.height = 20
    self.width = 20
    self.snakes = {}
    self.you = { 'id' :'1', 'body': [], 'health': 100}

  def testStart(self):
    with boddle(json='{"game":"myid"}'):
        startResponse = start()
        print 'start %s' % startResponse
        self.assertEqual(startResponse, '{"color": "red"}')

  def testMoveInitial(self):
    with boddle(json=self.generateMoveRequest(
        '____________________\n' +
        '________2______F____\n' +
        '____________________\n' +
        '____________F_______\n' +
        '____________________\n' +
        '___F________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________________\n' +
        '__________1_________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________F_______\n' +
        '____________________\n' +
        '____________________\n' +
        '________3___________\n' +
        '____________________\n' +
        '____________F_______\n' +
        '____________________')):
      moveResponse = move()
      self.assertEqual(moveResponse, '{"move": "up"}')

  def testMoveTopWall(self):
    with boddle(json=self.generateMoveRequest(
        '___________1________\n' +
        '________2______F____\n' +
        '____________________\n' +
        '____________F_______\n' +
        '____________________\n' +
        '___F________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________F_______\n' +
        '____________________\n' +
        '____________________\n' +
        '________3___________\n' +
        '____________________\n' +
        '____________F_______\n' +
        '____________________')):
      moveResponse = move()
      self.assertEqual(moveResponse, '{"move": "right"}')

  def testMoveTopRightWall(self):
    with boddle(json=self.generateMoveRequest(
        '___________________1\n' +
        '________2______F____\n' +
        '____________________\n' +
        '____________F_______\n' +
        '____________________\n' +
        '___F________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________F_______\n' +
        '____________________\n' +
        '____________________\n' +
        '________3___________\n' +
        '____________________\n' +
        '____________F_______\n' +
        '____________________')):
      moveResponse = move()
      self.assertEqual(moveResponse, '{"move": "down"}')

  def testMoveBottomRightWall(self):
    with boddle(json=self.generateMoveRequest(
        '____________________\n' +
        '________2______F____\n' +
        '____________________\n' +
        '____________F_______\n' +
        '____________________\n' +
        '___F________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________F_______\n' +
        '____________________\n' +
        '____________________\n' +
        '________3___________\n' +
        '____________________\n' +
        '____________F_______\n' +
        '___________________1')):
      moveResponse = move()
      self.assertEqual(moveResponse, '{"move": "left"}')

  def testMoveBottomLeftWall(self):
    with boddle(json=self.generateMoveRequest(
        '____________________\n' +
        '________2______F____\n' +
        '____________________\n' +
        '____________F_______\n' +
        '____________________\n' +
        '___F________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________F_______\n' +
        '____________________\n' +
        '____________________\n' +
        '________3___________\n' +
        '____________________\n' +
        '____________F_______\n' +
        '1___________________')):
      moveResponse = move()
      self.assertEqual(moveResponse, '{"move": "up"}')

  def testMoveTopLeftWall(self):
    with boddle(json=self.generateMoveRequest(
        '1___________________\n' +
        '________2______F____\n' +
        '____________________\n' +
        '____________F_______\n' +
        '____________________\n' +
        '___F________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________________\n' +
        '____________F_______\n' +
        '____________________\n' +
        '____________________\n' +
        '________3___________\n' +
        '____________________\n' +
        '____________F_______\n' +
        '____________________')):
      moveResponse = move()
      self.assertEqual(moveResponse, '{"move": "right"}')

  def generateMoveRequest(self, asciiBoard):
    moveRequest = {}
    self.addToil(moveRequest)
    self.convert(moveRequest,
        asciiBoard
    )
    moveRequest['you'] = self.you
    return moveRequest

  def convert(self, moveRequest, asciiPicture):
    moveRequest['board'] = {}
    moveRequest['board']['height'] = self.height
    moveRequest['board']['width'] = self.width
    moveRequest['board']['food'] = []
    moveRequest['board']['you'] = self.you
    for r_index, row in enumerate(asciiPicture.splitlines()):
        for c_index, char in enumerate(row):
            if char == '_':
                pass
            elif char == 'F':
                moveRequest['board']['food'].append({
                    'y': r_index,
                    'x': c_index
                })
            elif char == '1':
                moveRequest['board']['you']['body'].append({
                    'y': r_index,
                    'x': c_index
                })
            else:
                self.getOrCreateSnake(char)['body'].append({
                    'y': r_index,
                    'x': c_index
                })

    moveRequest['board']['snakes'] = self.snakes.values()
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
