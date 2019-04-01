#board.py
#This file has the "board" object, which is a useful data structure for implementing Frogger.

'''
SUBOBJECTS
Subobjects are parts of the game board that occupy exactly one square. Each subobject has an id, which is used for referencing it. The following is a list of data stored for each subobject.

Data for each subobject:
X: The X position of the subobject.
Y: The Y position of the subobject.
Segment: The segment state of the subobject. The idea here is that a larger object could hold multiple subobjects. For example, a long bus may have a front, middle, and back. Note: This has no effect on the board's handling of the object. 
    ALLOWED VALUES FOR SEGMENT
    -front
    -middle
    -back
    -na (Shorthand for "N/A", this means that there is no segment state.)
Direction: The direction of the subobject. 
    ALLOWED VALUES FOR DIRECTION
    -left
    -right
    -up
    -down
    -na (Shorthand for "N/A", this means that there is no direction state.)
Velocity: This stores the velocity of the subobject. The velocity is stored in a 2-tuple (IE '(a, b)'). The first element of the velocity is the change in x coordinate every time .update() is called. The second is the change in the y coordinate.

Some use cases that have been taken care of:
-Getting the state of a certain position
-Adding new subobjects
-Editting certain subobjects
-Rudimentary Physics: Collisions can be detected by calling .getCollisionsSinceLastUpdate()

Tips and tricks:
-Don't lose ids. These are the only way to refer to subobjects.
'''
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
    
    ##PUBLIC
    #General
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
            'velocity': (int) The velocity of the subobject at the position.
            'lane': (string) The lane at this coordinate.
        }
        @param x The x coordinate.
        @param y The y coordinate.
        @return The data structure, as detailed above.
        '''

        raise NotImplementedError
    
    def setLane(self, y, laneType):
        '''
        Sets the type of the lane along the given y axis.
        @param y The y coordinate to set.
        @param laneType A string indicating the type of lane that it is.
        '''

        raise NotImplementedError
    
    def update(self):
        '''
        Updates the board. Currently, this has the following functionalities:
        -Move all subobjects with a velocity.
        '''

        raise NotImplementedError
    
    def getCollisionsSinceLastUpdate(self):
        '''
        Returns a list of collisions that have occured since the last update. The format that is returned is a list of tuples. Each tuple contains two elements. The idea is that each element indicates the id of the subobject that collided with the other subobject.
        @return A list, as formatted above.
        '''

        raise NotImplementedError

    #SubObjects
    def addSubObject(self, id, type, x = 0, y = 0, segment = "na", direction = "na", velocity = (0, 0)):
        '''
        Adds a new subObject. Please see the documentation for subObjects for more details regarding each of the parameters... (TODO documentation regarding subObjects :P)
        @param id The id of the subObject.
        @param type The type of the subObject.
        @param x (optional) The initial X position. (defaults to 0)
        @param y (optional) The initial Y position. (defaults to 0)
        @param segment (optional) The segment. (defaults to 'na')
        @param direction (optional) The direction that it is going. (defaults to 'na')
        @param velocity (optional) The velocity (defaults to (0,0))
        '''

        raise NotImplementedError
    
    def getSubObject(self, id):
        '''
        Returns the subobject with the given id, formatted as a dictionary
        @param id The id of the subobject to lookup
        @raise KeyError If the id is not in the board.
        @return The subobject with this id.
        '''

        raise NotImplementedError

    def editSubObject(self, id, type = None, x = None, y = None, segment = None, direction = None, velocity = None):
        '''
        Edits the selected subobject.
        @param id The id to edit.
        @param {All other attributes} {The attribute}
        '''
        
        raise NotImplementedError

    def deleteSubObject(self, id):
        '''
        Deletes the subobject with the given id.
        @param id The id to delete
        '''

        raise NotImplementedError
