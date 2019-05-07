import sys
sys.path.append("..")

import unittest
import board

class boardTest(unittest.TestCase):
    def setUp(self):
        self.b = board.Board(10, 10)
    
    def tearDown(self):
        self.b = board.Board(10, 10)

    def test_placement(self):
        #Test will fail if the object was not added
        self.b.addSubObject(1, "test")
        self.b.getSubObject(1)
    
    def test_position(self):
        #Create subobject. We make sure it is at the right position.
        self.b.addSubObject(1, "a", 0, 0)
        x = self.b.getSubObject(1)['x']
        y = self.b.getSubObject(1)['y']
        self.assertEqual(x, 0)
        self.assertEqual(y, 0)
        
        #Move subobject. Is it still at the right place?
        self.b.editSubObject(1, x = 1, y = 1)
        x = self.b.getSubObject(1)['x']
        y = self.b.getSubObject(1)['y']
        self.assertEqual(x, 1)
        self.assertEqual(y, 1)
        self.assertEqual(self.b.getXY(0,0)['id'], None) #SURELY the object isn't where it was originally...right?
    
    def test_lanes(self):
        #Test the placement of lanes. The lane we set should be equal to the type we set it to, while others shouldn't be.
        self.b.setLane(1, "testLane")
        self.assertEqual(self.b.getXY(0,1)['lane'], "testLane")
        self.assertEqual(self.b.getXY(0,2)['lane'], "")
    
    def test_velocity(self):
        #Let's see if a SLOW moving object moves as expected.
        self.b.addSubObject(1, "testObject", x = 0, y = 0, velocity=(1,1)) #Our object to test.
        self.assertEqual(self.b.getSubObject(1)['x'], 0) #Do we start at the right X?
        self.assertEqual(self.b.getSubObject(1)['y'], 0) #Do we start at the right Y?
        self.b.update() #Alright, let's move everything.
        self.assertEqual(self.b.getSubObject(1)['x'], 1) #Do we end up at the right X?
        self.assertEqual(self.b.getSubObject(1)['y'], 1) #Do we end up at the right Y?
        self.b.update() #Once more, for good measure
        self.assertEqual(self.b.getSubObject(1)['x'], 2) #Do we end up at the right X?
        self.assertEqual(self.b.getSubObject(1)['y'], 2) #Do we end up at the right Y?

        #Let's see if a FAST moving object moves as expected.
        self.b.addSubObject(2, "testObject", x = 0, y = 0, velocity=(2,2)) #Our object to test.
        self.assertEqual(self.b.getSubObject(2)['x'], 0) #Do we start at the right X?
        self.assertEqual(self.b.getSubObject(2)['y'], 0) #Do we start at the right Y?
        self.b.update() #Alright, let's move everything.
        self.assertEqual(self.b.getSubObject(2)['x'], 2) #Do we end up at the right X?
        self.assertEqual(self.b.getSubObject(2)['y'], 2) #Do we end up at the right Y?
        self.b.update() #Once more, for good measure
        self.assertEqual(self.b.getSubObject(2)['x'], 4) #Do we end up at the right X?
        self.assertEqual(self.b.getSubObject(2)['y'], 4) #Do we end up at the right Y?
    
    def test_collisions(self):
        #First, a moving object collides with a non-moving object.
        self.b.addSubObject(1, "staticObject", x = 1, y = 0) #Create a static object.
        self.b.addSubObject(2, "movingObject", x = 0, y = 0, velocity=(2, 0)) #Create a moving object. As an added bonus, we have double velocity so as to test interpolation.
        self.assertEqual(self.b.getCollisionsSinceLastUpdate(), []) #SURELY there are no collisions yet, right?
        self.b.update() #Okay, now we move things.
        self.assertIn((2,1), self.b.getCollisionsSinceLastUpdate()) #Now, we check that they have collided.

        self.setUp()
        #Next, we test the collision of two moving object.
        self.b.addSubObject(3, "movingObject1", x = 1, y = 0, velocity=(0,2))
        self.b.addSubObject(4, "movingObject2", x = 0, y = 1, velocity=(2,0))
        self.assertEqual(self.b.getCollisionsSinceLastUpdate(), []) #SURELY there are no collisions yet, right?
        self.b.update() #Now move things
        self.assertIn((4,3),self.b.getCollisionsSinceLastUpdate()) #Now there should be a collision.

if __name__ == '__main__':
    unittest.main()