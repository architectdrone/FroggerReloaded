#game logic for Frogger
import board as b
import random

#PUBLIC GLOBALS
FROGGER_INITIAL_X = 0
FROGGER_INITIAL_Y = 0
SIZE_X = 10
SIZE_Y = 10

#PRIVATE GLOBALS
myBoard = b.Board(1, 1)
next_id = 1 #This is the next available id. Everytime we add a new subobject, we increment this id, and use the one that was there. We start at 1 so as to reserve 0 for the frog.
frog_id = 0 #This is the id of the frog. We must reserve just 0.
obstacle_ids = [] #This is a list of ids representing things that are dangerous to frogger. If there is a collision with id 0 (frogger) and one of these, frogger is dead!
platform_ids = [] #This is a list of ids representing things that are platforms.
dangerous_lane = [] #Lanes that kill, if not on a platform.
initialize(SIZE_X, SIZE_Y)

#PUBLIC FUNCTIONS
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

#PRIVATE FUNCTIONS
#No touchy
def generateBasic():
    '''
    Generates a basic game board. This game board has clusters of roads and swamps. Roads produce cars, swamps produce logs.
    '''
    #Some parameters. Since there should be clusters, what shout the minimum and maximum sizes of said clusters be?
    global myBoard, dangerous_lane, SIZE_Y
    GRASS_MIN = 1
    GRASS_MAX = 4
    ROAD_MIN = 2
    ROAD_MAX = 4
    SWAMP_MIN = 1
    SWAMP_MAX = 3

    #More parameters. What objects are available to enter from lane edges? Format as below:
    '''
    availableObjects = 
    [
        {
            "type": The type of the object.
            "directions": The possible directions. It is a list. Valid: ['left'], ['right'], ['left', 'right']
            "visableDirection": Whether or not the image can display the direction. A boolean. If not, the subobject has "na".
            "segments": A list of segments. For example ['front', 'middle', 'back']
            "speed": The speep of the object.
            "cooldown": Time between new ones entering.
            "lane": What lane it is available for. ("grass", "road", or "swamp")
        }
    ]
    '''
    #All this is mostly just for example
    availableMOLs = [
        {
            "type": "car",
            "directions": ["left", "right"],
            "visableDirection": True,
            "segments": ['na'],
            "speed": 3,
            "cooldown": 5,
            "lane": "road"
        },
        {
            "type": "log",
            "directions": ["left"],
            "visableDirection": True,
            "segments": ['na'],
            "speed": 1,
            "cooldown": 3,
            "lane": "swamp"
        }
    ]
    currentlyPlacing = "g" #Stores which cluster we are placing. "g" for grass, "r" for road, "s" for swamp. duh.
    toPlace = random.randrange(GRASS_MIN, GRASS_MAX)
    for y in range(SIZE_Y):
        if (y == SIZE_Y-1):
            myBoard.setLane("grass")
        if currentlyPlacing = "g":
            toPlace-=1
            myBoard.setLane("grass")
            if toPlace == 0:
                currentlyPlacing = random.choice(['s', 'r'])
                if currentlyPlacing == 's':
                    toPlace = random.randrange(SWAMP_MIN, SWAMP_MAX)
                elif currentlyPlacing == 'r':
                    toPlace = random.randrange(ROAD_MIN, ROAD_MAX)
        elif currentlyPlacing = "s":
            toPlace-=1
            myBoard.setLane("swamp")
            dangerous_lane.append(y) #Swamps are dangerous
            chooseMovingObjectLane(y, "swamp", availableMOLs)
            if toPlace == 0:
                currentlyPlacing = random.choice(['g', 'r'])
                if currentlyPlacing == 'g':
                    toPlace = random.randrange(GRASS_MIN, GRASS_MAX)
                elif currentlyPlacing == 'r':
                    toPlace = random.randrange(ROAD_MIN, ROAD_MAX)
        elif currentlyPlacing = "r":
            toPlace-=1
            myBoard.setLane("road")
            chooseMovingObjectLane(y, "road", availableMOLs)
            if toPlace == 0:
                currentlyPlacing = random.choice(['g', 's'])
                if currentlyPlacing == 'g':
                    toPlace = random.randrange(GRASS_MIN, GRASS_MAX)
                elif currentlyPlacing == 's':
                    toPlace = random.randrange(SWAMP_MIN, SWAMP_MAX)

def chooseMovingObjectLane(self, y, laneType, options):
    '''
    Chooses a moving object lane that works with the lane from the options, and adds it to the moving object lane variable
    '''
    global movingObjectLanes

    availableMOLs = [i for i in options if options['lane'] == laneType] #All MOLs that fit in with the current laneType
    currentMOL = random.choice(availableMOLs) #The chosen MOL
    MOLEntry = {
        "y": y,
        "direction": random.choice(currentMOL['directions']),
        "speed": currentMOL['speed'],
        "segments": currentMOL['segments'],
        "type": currentMOL['type'],
        "cooldown": currentMOL['cooldown'],
        "untilNext": random.randrange(1, currentMOL['cooldown']), #Just so that not everything is in sync.
        "entering": False,
        "whichSegment": 0
    }
    movingObjectLanes.append(MOLEntry)

def movingObjectLanes():
    '''
    Define lanes with moving objects
    '''
    movingObjectLane = {
            'type' : type,
            'y': y,
            'direction': direction,
            'speed' : speed,
            'segment' : segment,
            'coolDown' : coolDown,
            'untilNext' : untilNext,
            'entering' : entering,
            'whichSegment' : whichSegment
        }
    
    return movingObjectLane
    

def update():
    '''
    Updates moving subobjects in the lane
    '''
    global myBoard,next_id
    for lane in movingObjectLanes():
        if lane['entering']:
            myBoard.addSubObject(next_id, lane['type'], segment=lane['segments'][lane['whichSegment']], )
            next_id+=1
            if (lane['whichSegment'] > len((lane['segments'])-1)):
                lane['entering'] = False
                lane['untilNext'] = lane['coolDown']
                
        else:
            lane['untilNext'] -= 1
            if (lane['untilNext'] == 0):
                lane['entering'] = True
                lane['whichSegment'] = 0


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

def getInteractions():
    '''
    @return A list of all ids that frogger has either collided with or is on top of.
    '''
    global myBoard, obstacle_ids, dangerous_lane, platform_ids
    interactions = [] #This stores the id of everything that interacts with frogger
    interactions = getFrogIntersect() #First we populate it with everything the frog is intersecting.
    collisions = getFrogCollisions() #All of the collisions with frogger
    if len(collisions) != 0: #If there is more than one element
        interactions.append(list(getFrogCollisions()[0])) #We then append everything that has collided with the frog. Now, we know that this is formatted as a list of tuples, but there should only be one element in this list
    #Otherwise, nothing collides with ya boi frogger
    interactions = list(dict.fromkeys(interactions)) #Remove duplicates
    return interactions

def getLifeStatus():
    '''
    @return True if the frog is still alive, false otherwise.
    '''

    #Subobject Testing
    interactions = getInteractions()
    for i in obstacle_ids:
        if i in interactions:
            return False
    
    #Lane testing
    frog_y = myBoard.getSubObject(frog_id)['y'] #The y coordinate of frogger
    if frog_y in dangerous_lane: #If frogger is in a dangerous lane, check if we are on a plaform.
        dead = True
        for i in platform_ids:
            if i in interactions:
                dead = False
                break
        if dead:
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

def getCollisions():
    '''
    Return collisions with frog
    TODO
    ''' 
    global myBoard, frog_id
    collisions = myBoard.getCollisionsSinceLastUpdate()
    toReturn = [i for i in collisions if frog_id in i]
    return toReturn
