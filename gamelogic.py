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
dangerous_lane = [] #Lanes that kill, if not on a platform. Each element is the y coordinate of the lane.
movingObjectLanes = [] #Lanes that produce objects. There is a specific internal structure to this list, see chooseMovingObjectLane for deatils
isDead = False #Are we dead?

#PUBLIC FUNCTIONS
def initialize():
    '''
    Initializes game board
    '''
    global myBoard, FROGGER_INITIAL_X, FROGGER_INITIAL_Y, frog_id, dangerous_lane
    
    myBoard = b.Board(SIZE_X, SIZE_Y)
    myBoard.addSubObject(frog_id, "frog", x = FROGGER_INITIAL_X, y = FROGGER_INITIAL_Y, direction="up")
    dangerous_lane = []

    generateBasic()

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
            myBoard.setLane(y, "grass")
        elif currentlyPlacing == "g":
            toPlace-=1
            myBoard.setLane(y, "grass")
            if toPlace == 0:
                currentlyPlacing = random.choice(['s', 'r'])
                if currentlyPlacing == 's':
                    toPlace = random.randrange(SWAMP_MIN, SWAMP_MAX)
                elif currentlyPlacing == 'r':
                    toPlace = random.randrange(ROAD_MIN, ROAD_MAX)
        elif currentlyPlacing == "s":
            toPlace-=1
            myBoard.setLane(y, "swamp")
            dangerous_lane.append(y) #Swamps are dangerous
            chooseMovingObjectLane(y, "swamp", availableMOLs)
            if toPlace == 0:
                currentlyPlacing = random.choice(['g', 'r'])
                if currentlyPlacing == 'g':
                    toPlace = random.randrange(GRASS_MIN, GRASS_MAX)
                elif currentlyPlacing == 'r':
                    toPlace = random.randrange(ROAD_MIN, ROAD_MAX)
        elif currentlyPlacing == "r":
            toPlace-=1
            myBoard.setLane(y, "road")
            chooseMovingObjectLane(y, "road", availableMOLs)
            if toPlace == 0:
                currentlyPlacing = random.choice(['g', 's'])
                if currentlyPlacing == 'g':
                    toPlace = random.randrange(GRASS_MIN, GRASS_MAX)
                elif currentlyPlacing == 's':
                    toPlace = random.randrange(SWAMP_MIN, SWAMP_MAX)

def chooseMovingObjectLane(y, laneType, options):
    '''
    Chooses a moving object lane that works with the lane from the options, and adds it to the moving object lane variable.
    Structure of a moving object lane:
    {
        'y': The y coordinate of the lane.
        'direction': The direction of the objects in the lane. left or right.
        'speed': The speed of the objects in the lane.
        'segments': The segments in the object. This is a list. The first element is the one to emerge first. Example: ['front', 'middle','back']
        'type': The type of the object.
        'cooldown': How long to wait until the next object emerges.
        'untilNext': How long until the next object emerges. (USED ONLY BY UPDATE)
        'entering': Whether or not the object is entering. (USED ONLY BY UPDATE)
        'whichSegment': The index of segments that is emerging. (USED ONLY BY UPDATE)
    }
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
    
def update():
    '''
    Updates board, moving subobjects in the lane, and the frog.
    '''
    global myBoard,next_id, SIZE_X
    #Board-level update
    myBoard.update()

    #Causing objects to enter.
    for lane in movingObjectLanes: #Check each moving object lane.
        if lane['entering']: #If we are in the entering state.
            #Since the velocity and the position are based off of the direction, we compute them here. If the object is moving left, it has a positive velocity, if not, negative.
            velocityX = 0
            positionX = 0
            if lane['direction'] == "right":
                velocityX = lane['speed']
                positionX = 0
            elif lane['direction'] == "left":
                velocityX = -1*lane['speed']

                positionX = SIZE_X-1
            
            
            myBoard.addSubObject(next_id, lane['type'], y=lane['y'], segment=lane['segments'][lane['whichSegment']], direction=lane['direction'],velocity = (velocityX, 0),x = positionX)

            lane['whichSegment']+=1
            next_id+=1 #Increment the next_id, as we should everytime we create a subobject.
            if (lane['whichSegment'] > len((lane['segments'])-1)): #Now we test to make sure that we haven't run out of segments. This is determined by the segment that we are on, according to whichSegment, and the length of list of segments.
                lane['entering'] = False #If we have, entering mode ends.
                lane['untilNext'] = lane['coolDown'] #We also reset the cooldown.
                
        else: #If we are not in the entering state.
            lane['untilNext'] -= 1 #We count down by one.
            if (lane['untilNext'] == 0): #If we have reach 0, the countdown has expired.
                lane['entering'] = True #In that case we start entering mode.
                lane['whichSegment'] = 0 #We also reset whichSegment.

    #Do a frog check.
    frogCheck()

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

def frogCheck():
    '''
    Do all checks. Sees if we are dead, and sets the frog's velocity based off of the platform that he is (or isn't) on.
    '''
    global isDead
    dead = False

    #Subobject Testing - Test to see if we have collided with an obstacle
    interactions = getInteractions()
    for i in interactions:
        if i in obstacle_ids:
            dead = True

    
    #Lane testing --Test to see if we are on a dangerous lane. If we are, test to see if we are on a platform. If we are, set froggers velocity to be the velocity of the platform.
    frog_y = myBoard.getSubObject(frog_id)['y'] #The y coordinate of frogger
    myBoard.editSubObject(frog_id, velocity=(0,0)) #Pre set the velocity to 0.
    if frog_y in dangerous_lane: #If frogger is in a dangerous lane, check if we are on a plaform.
        laneDead = True
        for i in platform_ids:
            if i in interactions: #If we are standing on a platform...
                laneDead = False
                platformVelocity = myBoard.getSubObject(i)['velocity'] #Get the velocity of the platform.
                myBoard.editSubObject(frog_id, velocity=platformVelocity) #Set our velocity to the velocity of the platform.
                break
        if laneDead:
            dead = True

    isDead = dead
