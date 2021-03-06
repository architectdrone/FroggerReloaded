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
class Board():
    def __init__(self, x, y):
        '''
        Creates and inititalizes the board.
        @param x The size of the board in the x direction.
        @param y The size of the board in the y direction.
        '''
        self.size = (x, y) #The size of the board. Obviously, size[0] is the size in the x direction while size[1] is size in the y direction.
        self.lanes = ["" for i in range(y)] #This is a list of all of the lane types of the board. Thus, lanes[5] is a string representing the lane type at y = 5. (This is a list comprehension, by the way.)
        self.subObjects = [] #All subobjects in the board. Stored in dictionaries.
        self.collisionsSinceLastUpdate = []

    ##PUBLIC
    #General
    def getXY(self, x, y):
        '''
        Returns a data structure representing what is at the requested x and y coordinates.
        The data structure is a dictionary, formatted like so:
        return = 
        {
            'type': (string) The type of the subobject found at this coordinate. If there is no subobject, the string is empty.  (A List)
            'segment': (string) The segment of the subobject that is found at this coordinate. If there is a subobject there, this will be one of the following: [front, middle, back, na]. If there isn't, this will be an empty string. (A List)
            'direction': (string) The direction of the subobject that is found at this coordinate. If there is a subobject there, this will be one of the following: [left, right, up, down, na]. If there isn't, this will be an empty string. (A List)
            'id': (int) The id of the subobject that is found at this coordinate. If there is no sub object, this will be -1. (A List)
            'velocity': (int) The velocity of the subobject at the position. (A List)
            'lane': (string) The lane at this coordinate.
        }
        @param x The x coordinate.
        @param y The y coordinate.
        @return The data structure, as detailed above.
        '''

        theSubObject = self.getSubObjectAtPosition(x, y)
        if theSubObject is not None:
            toReturn = {
                'type': theSubObject['type'],
                'segment': theSubObject['segment'],
                'direction': theSubObject['direction'],
                'id': theSubObject['id'],
                'velocity': theSubObject['velocity'],
                'lane': self.lanes[y]
            }
        else:
            toReturn = {
                'type': [],
                'segment': [],
                'direction': [],
                'id': [],
                'velocity': [],
                'lane': self.lanes[y]
            }
        return toReturn
    
    def resetBoard(self):
        '''
        Clears everything in the board.
        '''
        self.subObjects = []
        self.collisionsSinceLastUpdate = []

    def setLane(self, y, laneType):
        '''
        Sets the type of the lane along the given y axis.
        @param y The y coordinate to set.
        @param laneType A string indicating the type of lane that it is.
        '''

        self.lanes[y] = laneType

    def update(self):
        '''
        Updates the board. Currently, this has the following functionalities:
        -Move all subobjects with a velocity.
        '''

        self.updatePosition()
    
    def getCollisionsSinceLastUpdate(self):
        '''
        Returns a list of collisions that have occured since the last update. The format that is returned is a list of tuples. Each tuple contains two elements. The idea is that each element indicates the id of the subobject that collided with the other subobject.
        @return A list, as formatted above.
        '''
        return self.collisionsSinceLastUpdate

    def flushCollisions(self):
        '''
        Gets rid of all collisions in getCollisionsSinceLastUpdate()
        '''
        self.collisionsSinceLastUpdate = []

    def printAllSubObjects(self):
        print("----Here's all of the subobjects!----")
        for i in self.subObjects:
            print(f"{i['id']}: TYPE = {i['type']} SEGMENT = {i['segment']} X = {i['x']} Y = {i['y']} VELOCITY = {i['velocity']}")

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
        newSubObject = {
            'id': id,
            'type': type,
            'x': x,
            'y': y,
            'segment': segment,
            'direction': direction,
            'velocity': velocity
        }
        self.subObjects.append(newSubObject)
    
    def getSubObject(self, id):
        '''
        Returns the subobject with the given id, formatted as a dictionary
        @param id The id of the subobject to lookup
        @raise AssertationError If the id is not in the board.
        @return The subobject with this id.
        '''

        #There may be a cleaner way to do this, but I don't care enough to find out.
        results = [i for i in self.subObjects if i['id'] == id]
        assert len(results) != 0, f"The id {id} could not be found."
        return results[0]

    def editSubObject(self, id, type = None, x = None, y = None, segment = None, direction = None, velocity = None):
        '''
        Edits the selected subobject.
        @param id The id to edit.
        @param {All other attributes} {The attribute}
        @raise KeyError If the ID isn't present
        '''
        
        #Get the index of the subObject
        subObjectIndex = self.indexOfSubObject(id)
        if (type != None):
            self.subObjects[subObjectIndex]['type'] = type
        if (x != None):
            self.subObjects[subObjectIndex]['x'] = x
        if (y != None):
            self.subObjects[subObjectIndex]['y'] = y
        if (segment != None):
            self.subObjects[subObjectIndex]['segment'] = segment
        if (direction != None):
            self.subObjects[subObjectIndex]['direction'] = direction
        if (velocity != None):
            self.subObjects[subObjectIndex]['velocity'] = velocity

    def deleteSubObject(self, id):
        '''
        Deletes the subobject with the given id.
        @param id The id to delete
        @raise KeyError If the ID isn't present
        '''
        subObjectIndex = self.indexOfSubObject(id)
        self.subObjects.pop(subObjectIndex)

    ##PRIVATE
    def indexOfSubObject(self, id):
        '''
        Get the index of the subobject.
        '''

        for n, i in enumerate(self.subObjects):
            if i['id'] == id:
                return n
        raise KeyError

    def updatePosition(self):
        '''
        Update positions based off of velocity
        '''
        particles = [{"id":i['id'],"current_x":i['x'], "current_y":i['y'], "remaining_x_movement":i['velocity'][0], "remaining_y_movement":i['velocity'][1]} for i in self.subObjects]
        self.collisionsSinceLastUpdate = []

        allDone = False #Tells us if we are done. This is False when movement is possible.
        positionLog = [{"pos":(i['current_x'],i['current_y']),"id":i['id']} for i in particles] #Records every single position where an ID has been. A list of dictionaries. Initializes to initial conditions.{"pos":(x,y),"id":id}
        #x and y overlaps are lists of lists. Each element represents an x or y coordinate. For example, everything at x=3 is stored in x_overlaps[3].
        out_of_bounds = []
        while not allDone: #We do this until we determine that no more movement is possible.
            allDone = True #Assume that we are done

            #Move everything
            newParticles = []
            for index, element in enumerate(particles): 
                #Move in the x direction
                new_x = element['current_x']
                new_y = element['current_y']
                new_remaining_x_movement = element['remaining_x_movement']
                new_remaining_y_movement = element['remaining_y_movement']
                    
                if element['remaining_x_movement'] != 0:
                    allDone = False #Movement is still possible in this case.
                    if element['remaining_x_movement'] > 0:
                        new_x+=1
                        new_remaining_x_movement-=1
                    else:
                        new_x-=1
                        new_remaining_x_movement+=1
                #Move in the y direction
                if element['remaining_y_movement'] != 0:
                    allDone = False #Movement is still possible in this case.
                    if element['remaining_y_movement'] > 0:
                        new_y+=1
                        new_remaining_y_movement-=1
                    else:
                        new_y-=1
                        new_remaining_y_movement+=1
                #Add to position log
                if not (particles[index]['current_x'] >= self.size[0] or particles[index]['current_x'] < 0 or particles[index]['current_y'] >= self.size[1] or particles[index]['current_y'] < 0):
                    positionLog.append({"pos":(new_x, new_y), "id":element['id']})
                else:
                    out_of_bounds.append(element['id'])
                
                #Append to new list
                newParticles.append({"id":element['id'],"current_x":new_x, "current_y":new_y, "remaining_x_movement":new_remaining_x_movement, "remaining_y_movement":new_remaining_y_movement})
            particles = newParticles
        #Check for collisions.
        for toCheck in positionLog:
            for checkAgainst in positionLog:
                if checkAgainst['pos'] == toCheck['pos'] and toCheck['id'] != checkAgainst['id']: #If they were at the same position, and if they were different objects.
                    if (checkAgainst['id'], toCheck['id']) not in self.collisionsSinceLastUpdate and (toCheck['id'], checkAgainst['id']) not in self.collisionsSinceLastUpdate:
                        self.collisionsSinceLastUpdate.append((checkAgainst['id'], toCheck['id']))

        #Now, we must update the positions
        for i in particles:
            self.editSubObject(i['id'], x=i['current_x'], y=i['current_y'])
        
        #Remove everything that is out of bounds
        for i in out_of_bounds:
            try:
                self.deleteSubObject(i)
            except:
                continue
        
        """ #Remove non-collisions from list of collisions. (Yes, this is neccesary)
        i = 0
        while True:
            if i == len(self.collisionsSinceLastUpdate)-1:
                break
            if self.collisionsSinceLastUpdate[i] == () or len(self.collisionsSinceLastUpdate[i]) != 2:
                self.collisionsSinceLastUpdate.pop(i)
            else:
                i+=1 """


    def getSubObjectAtPosition(self, x, y):
        toReturn = {
            'type': [],
            'segment': [],
            'direction': [],
            'id': [],
            'velocity': []
        }
        for i in self.subObjects:
            if i['x'] == x and i['y'] == y:
                toReturn['type'].append(i['type'])
                toReturn['segment'].append(i['segment'])
                toReturn['direction'].append(i['direction'])
                toReturn['id'].append(i['id'])
                toReturn['velocity'].append(i['velocity'])
        if toReturn['type'] == []:
            toReturn['type'] = None
            toReturn['segment'] = None
            toReturn['direction'] = None
            toReturn['id'] = None
            toReturn['velocity'] = None
        return toReturn