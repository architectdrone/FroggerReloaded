#game logic for Frogger
import board as b

'''
TODO
SUBOBJECTS
-log
-car, truck
-lanes: river, road
-turtle
-frog

SCORE

Number of LIVES
'''

myBoard = b.Board(1, 1)
def initialize(x_size, y_size):
    '''
    Initializes game board
    @param x_size x dimension of board
    @param y_size y dimension of board
    '''
    myBoard = b.Board(x_size, y_size)

    #place subobjects


def Obstacle
    

class Frog():
    def __init__(self, x, y):
        '''
        Initializes frog object
        @param x The current x coordinate of the frog
        @param y The current y coordinate of the frog
        @throw IndexError if requested coordinate is off the board.
        '''
        self.x_init = x #initial x coordinate
        self.y_init = y #initial y coordinate
    
    def reset_pos(self):
        '''
        Resets the frog to initial position
        @param self
        '''
        self.x = self.x_init
        self.y = self.y_init
    
    def getCoordinate(x, y):
        '''
        Get the state of the current position of the frog, TODO
        @param x The current x coordinate of the frog
        @param y The current y coordinate of the frog
        @throw IndexError if requested coordinate is off the board. 
        @return state of the frog
        '''
        global myBoard
        currentPos = myBoard.getXY(x, y) #This is already formatted as a dictionary
        return currentPos

    def move(self, x, y):
        '''
        Movement of frog, TODO
        @param x The current x coordinate of the frog
        @param y The current y coordinate of the frog
        @throw IndexError if requested coordinate is off the board. 
        @return update position of frog
        '''
        global myBoard
        inRange = lambda x, y: (x >= 0) and (x < myBoard.x_size) and (y >= 0) and (y < myBoard.y_size)

            def up():
                self.y = self.y + 1
            def down():
                self.y = self.y - 1
            def right():
                self.x = self.x + 1
            def left():
                self.x = self.x - 1

            #prevents frog from moving out of bounds
            if self.x < 0: 
                self.x = 0
            if self.y < 0:
                self.y = 0    

        def interact()
        '''
        What happens when the frog encounters a subobject, TODO
        @param x The current x coordinate of the frog
        @param y The current y coordinate of the frog
        '''



def road() :
    setLane(self, y, 'road')

def river() :
    setLane(self, y, 'river')