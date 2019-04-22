import sys
sys.path.append("..")

import unittest
import gamelogic

class gamelogicTest(unittest.TestCase):
    def setUp(self):
        self.g = gamelogic.game(10, 10)
    
    def tearDown(self):
        self.g = gamelogic.game(10, 10)
    
    def test_frogUp(self):
        self.g.myBoard.addSubObject(0,"frog", 0, 0)
        self.g.frogUp()
        y = self.g.myBoard.getSubObject(0)['y']
        self.assertEqual(y, 1)

        self.g.myBoard.editSubObject(0,"frog", 0, 9)
        self.g.frogUp()
        y = self.g.myBoard.getSubObject(0)['y']
        self.assertEqual(y, 0)

    def test_frogDown(self):
        self.g.myBoard.addSubObject(0,"frog", 0, 8)
        self.g.frogDown()
        y = self.g.myBoard.getSubObject(0)['y']
        self.assertEqual(y, 7)

    def test_frogLeft(self):
        self.g.myBoard.addSubObject(0,"frog", 1, 0)
        self.g.frogLeft()
        x = self.g.myBoard.getSubObject(0)['x']
        self.assertEqual(x, 0)

    def test_frogRight(self):
        self.g.myBoard.addSubObject(0,"frog", 1, 0)
        self.g.frogRight()
        x = self.g.myBoard.getSubObject(0)['x']
        self.assertEqual(x, 1)

'''
    def test_score(self):
        self.g.myBoard.addSubObject(0,"frog", 0, 9)
        self.g.game.frogUp()
        y = self.g.myBoard.getSubObject(0)['y']
        self.assertEqual(self.g.score, 1)
    
    def test_frogIntersect(self):
        self.g.myBoard.addSubObject(0,"frog", 1, 1)
        self.g.myBoard.addSubObject(1,"testObject", 1, 1)
        self.assertEqual(self.g.getFrogIntersect, 1)
    
    def test_getFrogCollisions(self):
        self.g.myBoard.addSubObject(0,"frog", 1, 1)
        self.g.myBoard.addSubObject(1,"testObject1", 1, 1)
        self.g.myBoard.addSubObject(2,"testObject2", 1, 1)
        self.assertEqual(self.g.getFrogCollisions, ["testObject1" , "testObject2"])
    
    def test_frogCheck(self): #incomplete
        self.g.myBoard.addSubObject(0,"frog", 1, 1)
        self.g.myBoard.addSubObject(1, "truck", 1, 1)
        self.assertEqual(self.g.frogCheck, False)
  '''  
    '''
    TO-BE tested
    Public functions:
        initialize
        update
        getXY
        
    '''


