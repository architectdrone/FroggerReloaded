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
        self.g.frogUp()
        assert 'type' in self.g.getXY(0,1) and self.g.getXY(0,1)['type'] is not None #Test if there is a subobject at the position.
        self.assertEqual(self.g.getXY(0,1)['type'][0], 'frog') #Test if the subobject there is frog.

    def test_frogDown(self):
        self.g.frogDown()
        assert 'type' in self.g.getXY(0,0) and self.g.getXY(0,0)['type'] is not None#Test if there is a subobject at the position.
        self.assertEqual(self.g.getXY(0,0)['type'][0], 'frog') #Test if the subobject there is frog.

        self.g.init_x = 1
        self.g.init_y = 1
        self.g.initialize()
        self.g.frogDown()
        assert 'type' in self.g.getXY(1,0) and self.g.getXY(1,0)['type'] is not None #Test if there is a subobject at the position.
        print(self.g.getXY(1,0))
        self.assertEqual(self.g.getXY(1,0)['type'][0], 'frog') #Test if the subobject there is frog.

    def test_frogRight(self):
        self.g.frogRight()
        assert 'type' in self.g.getXY(1,0) and self.g.getXY(1,0)['type'] is not None #Test if there is a subobject at the position.
        self.assertEqual(self.g.getXY(1,0)['type'][0], 'frog') #Test if the subobject there is frog.

    def test_frogLeft(self):
        self.g.frogLeft()
        assert 'type' in self.g.getXY(0,0) and self.g.getXY(0,0)['type'] is not None#Test if there is a subobject at the position.
        self.assertEqual(self.g.getXY(0,0)['type'][0], 'frog') #Test if the subobject there is frog.

        self.g.init_x = 1
        self.g.init_y = 1
        self.g.initialize()
        self.g.frogLeft()
        assert 'type' in self.g.getXY(0,1) and self.g.getXY(0,1)['type'] is not None #Test if there is a subobject at the position.
        self.assertEqual(self.g.getXY(0,1)['type'][0], 'frog') #Test if the subobject there is frog.


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
    
    TO-BE tested
    Public functions:
        initialize
        update
        getXY
        
    '''


if __name__ == '__main__':
    unittest.main()