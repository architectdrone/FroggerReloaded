#board.py
#This file has the "board" object, which is a useful data structure for implementing Frogger.

class board():
    def __init__(self, x, y):
        '''
        Creates and inititalizes the board.
        @param x The size of the board in the x direction.
        @param y The size of the board in the y direction.
        '''
        self.size = (x, y) #The size of the board. Obviously, size[0] is the size in the x direction while size[1] is size in the y direction.
        self.lanes = ["" for i in range(y)] #This is a list of all of the lane types of the board. Thus, lanes[5] is a string representing the lane type at y = 5. (This is a list comprehension, by the way.)
        self.subObjects = [] #All subobjects in the board. Subobjects are objects tht fit within a single square.
    
    def getXY(self, x, y):
        '''
        Returns a data structure representing what is at the requested x and y coordinates.
        The data structure is a dictionary, formatted like so:
        return = 
        {
            'type': (string) The type of the subobject found at this coordinate. If there is no subobject, the string is empty.
            'segment': (string) The segment of the subobject that is found at this coordinate. If there is a subobject there, this will be one of the following: [front, middle, back, na]. If there isn't, this will be an empty string.
            'direction': (string) The direction of the subobject that is found at this coordinate. If there is a subobject there, this will be one of the following: [left, right, up, down, na]. If there isn't, this will be an empty string.
            'id': (int) The id of the subobject that is found at this coordinate. If there is no sub object, this will be -1.
            'lane': (string) The lane at this coordinate.
        }
        @param x The x coordinate.
        @param y The y coordinate.
        @return The data structure, as detailed above.
        '''

        raise NotImplementedError
    
    def get