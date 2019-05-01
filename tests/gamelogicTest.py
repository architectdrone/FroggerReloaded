#test frog movement and score in game play
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

    def test_score(self):
        self.assertEqual(self.g.score(), 0)
        self.g.init_x = 0
        self.g.init_y = 9
        self.g.initialize() #set initial position to (0,9)
        self.g.frogUp()
        self.assertEqual(self.g.score(), 1) #score increments when moved up

if __name__ == '__main__':
    unittest.main()