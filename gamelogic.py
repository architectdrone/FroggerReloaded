#game logic for Frogger
import board as b

FROGGER_INITIAL_X = 0
FROGGER_INITIAL_Y = 0
SIZE_x = 10
SIZE_Y = 10

#PUBLIC
myBoard = b.Board(1, 1)
def initialize(x_size, y_size):
    '''
    Initializes game board
    @param x_size x dimension of board
    @param y_size y dimension of board
    '''
    global myBoard, FROGGER_INITIAL_X, FROGGER_INITIAL_Y, frog_id
    
    myBoard = b.Board(x_size, y_size)
    myBoard.addSubObject(frog_id, "frog", x = FROGGER_INITIAL_X, y = FROGGER_INITIAL_Y)
    #place subobjects and lanes using a procedural generation method.

next_id = 1 #This is the next available id. Everytime we add a new subobject, we increment this id, and use the one that was there. We start at 1 so as to reserve 0 for the frog.
frog_id = 0 #This is the id of the frog. We must reserve just 0.
obstacle_ids = [] #This is a list of ids representing things that are dangerous to frogger. If there is a collision with id 0 (frogger) and one of these, frogger is dead!
platform_ids = [] #This is a list of ids representing things that are platforms.
dangerous_lane = [] #Lanes that kill, if not on a platform.
initialize(SIZE_x, SIZE_Y)



def frogUp():
    '''
    Moves the frog up.
    '''
    global myBoard, frog_id
    theSubObject = myBoard.getSubObject(frog_id)
    current_x = theSubObject['x']
    current_y = theSubObject['y']
    myBoard.editSubObject(frog_id, x = current_x, y = current_y+1, direction = "up")
    frogCheck()

def frogDown():
    '''
    Moves the frog down.
    '''
    global myBoard, frog_id
    theSubObject = myBoard.getSubObject(frog_id)
    current_x = theSubObject['x']
    current_y = theSubObject['y']
    myBoard.editSubObject(frog_id, x = current_x, y = current_y-1, direction = "down")
    frogCheck()

def frogLeft():
    '''
    Moves the frog left.
    '''
    global myBoard, frog_id
    theSubObject = myBoard.getSubObject(frog_id)
    current_x = theSubObject['x']
    current_y = theSubObject['y']
    myBoard.editSubObject(frog_id, x = current_x-1, y = current_y, direction = "left")
    frogCheck()

def frogRight():
    '''
    Moves the frog right.
    '''
    global myBoard, frog_id
    theSubObject = myBoard.getSubObject(frog_id)
    current_x = theSubObject['x']
    current_y = theSubObject['y']
    myBoard.editSubObject(frog_id, x = current_x+1, y = current_y, direction = "right")
    frogCheck()

def getXY(x, y):
    '''
    Get the sprite that should be at X and Y. Returns in the following format:
    {
        'segment': The segment of the subobject at the XY. Present only if there is a subobject at XY.
        'type': The type of the subobject at the XY. Present only if there is a subobject at XY.
        'direction': The direction of the subobject at the XY. Present only if there is a subobject at XY.
        'lane': The lane at XY.
    }
    @return Information about the X and Y position, formatted as written above.
    '''
    global myBoard
    AtXY = myBoard.getXY(x, y)
    if AtXY['segment'] != "" :
        return {
            'segment': AtXY['segment'],
            'type': AtXY['type'],
            'direction': AtXY['direction'],
            'lane': AtXY['lane']
        }
    else:
        return {'lane': AtXY['lane']}

def frogReset():
    '''
    Resets position of frog
    '''
    global myBoard, frog_id
    myBoard.editSubObject(frog_id, x = FROGGER_INITIAL_X, y = FROGGER_INITIAL_Y, direction = "na")

##PRIVATE
def frogCheck():
    '''
    Runs whenever the frog moves.
    '''
    pass

def getFrogIntersect():
    '''
    @return The list of all things that intersect with the frog
    '''
    global myBoard, frog_id
    frog = myBoard.getSubObject(frog_id)
    frog_x = frog['x']
    frog_y = frog['y']

    allIDs = myBoard.getXY(frog_x, frog_y)['id']
    allIDs.pop(allIDs.index(frog_id))
    return allIDs

def getFrogCollisions():
    '''
    @return The list of things that have collided with the frog.
    '''
    global myBoard, frog_id
    allC = myBoard.getCollisionsSinceLastUpdate()
    allFrogC = [i for i in allC if frog_id in i]
    return allFrogC

def getLifeStatus():
    '''
    @return True if the frog is still alive, false otherwise.
    '''
    global myBoard, obstacle_ids, dangerous_lane

    #Subobject testing
    interactions = [] #This stores the id of everything that interacts with frogger
    interactions = getFrogIntersect() #First we populate it with everything the frog is intersecting.
    collisions = getFrogCollisions() #All of the collisions with frogger
    if len(collisions) != 0: #If there is more than one element
        interactions.append(list(getFrogCollisions()[0])) #We then append everything that has collided with the frog. Now, we know that this is formatted as a list of tuples, but there should only be one element in this list
    #Otherwise, nothing collides with ya boi frogger
    interactions = list(dict.fromkeys(interactions)) #Remove duplicates
    
    for i in obstacle_ids:
        if i in interactions:
            return False

def attach():
    '''
    If frog intersects with a log frog can attach, return True if attached
    TODO
    '''  
    attached = False
    global myBoard, frog_id, obstacle_ids
    if intersect == True:
        for i in obstacle_ids:
            obstacle = myBoard.getSubObject(obstacle_ids[i])
            if (obstacle['log']):
                v = obstacle['velocity']
                myBoard.editSubObject(frog_id, x = obstacle['x'], y = obstacle['y'], velocity = v)
                attached = True

    return attached
