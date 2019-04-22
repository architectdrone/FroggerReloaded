#game logic for Frogger
import board as b
import random
import math

class game():
    
    def __init__(self, x_size, y_size, init_x = 0, init_y = 0):
        '''
        Creates the game object. Sets up all non-strictly game related features (such as score) and creates the board.
        @param x_size The number of squares in the x direction.
        @param y_size The number of squares in the y direction.
        '''
        self.x_size = x_size
        self.y_size = y_size
        self.init_x = init_x
        self.init_y = init_y
        self.currentMinigame = "basic" #The minigame we are currently on. Allowed values are "basic", "lilypads", "invaders".
        self.initialize()
        self.displayCount = 0 #counts change in display

    #PUBLIC FUNCTIONS
    def initialize(self):
        '''
        Resets and initializes game board. Size is determined by global variables.
        '''
        self.next_id = 1 #This is the next available id. Everytime we add a new subobject, we increment this id, and use the one that was there. We start at 1 so as to reserve 0 for the frog.
        self.frog_id = 0 #This is the id of the frog. We must reserve just 0.
        self.obstacle_id = [] #This is a list of ids representing things that are dangerous to frogger. If there is a collision with id 0 (frogger) and one of these, frogger is dead!
        self.platform_id = [] #This is a list of ids representing things that are platforms.
        self.dangerous_lane = [] #Lanes that kill, if not on a platform. Each element is the y coordinate of the lane.
        self.wall_ids = [] #Things frogger can't move through, but don't kill him. Only currently used in the invaders minigame.
        self.enemy_ids = [] #The ids of enemies. Keep in mind that these are enemies from space invaders, don't mix up with obstacles!
        self.movingObjectLanes = [] #Lanes that produce objects. There is a specific internal structure to this list, see chooseMovingObjectLane for deatils
        self.isDead = False #Are we dead?

        self.myBoard = b.Board(self.x_size, self.y_size)
        self.myBoard.addSubObject(self.frog_id, "frog", x = self.init_x, y = self.init_y, direction="up")

        self.generateBasic() #Runs the board generator.

    def update(self):
        '''
        -Moves subobjects.
        -Checks if frog is still alive.
        -Move frog if on platform.
        -Causes new moving objects to enter lanes
        '''
        
        #Do a frog check.
        self.frogCheck()

        #Board-level update
        self.myBoard.update()

        #Causing objects to enter.
        for lane in self.movingObjectLanes: #Check each moving object lane.
            if lane['entering']: #If we are in the entering state.
                #Since the velocity and the position are based off of the direction, we compute them here. If the object is moving left, it has a positive velocity, if not, negative.
                velocityX = 0
                positionX = 0
                if lane['direction'] == "right":
                    velocityX = lane['speed']
                    positionX = 0
                elif lane['direction'] == "left":
                    velocityX = -1*lane['speed']

                    positionX = self.x_size-1
                
                
                self.myBoard.addSubObject(self.next_id, lane['type'], y=lane['y'], segment=lane['segments'][lane['whichSegment']], direction=lane['direction'],velocity = (velocityX, 0),x = positionX)
                current_id = self.next_id

                if lane['platform']:
                    self.platform_id.append(current_id)
                elif lane['obstacle']:
                    self.obstacle_id.append(current_id)
                
                lane['whichSegment']+=1
                self.next_id+=1 #Increment the self.next_id, as we should everytime we create a subobject.
                if (lane['whichSegment'] > len((lane['segments']))-1): #Now we test to make sure that we haven't run out of segments. This is determined by the segment that we are on, according to whichSegment, and the length of list of segments.
                    lane['entering'] = False #If we have, entering mode ends.
                    lane['untilNext'] = lane['cooldown'] #We also reset the cooldown.
                    
            else: #If we are not in the entering state.
                lane['untilNext'] -= 1 #We count down by one.
                if (lane['untilNext'] == 0): #If we have reach 0, the countdown has expired.
                    lane['entering'] = True #In that case we start entering mode.
                    lane['whichSegment'] = 0 #We also reset whichSegment.

        #self.myBoard.printAllSubObjects()

    def frogUp(self):
        '''
        Moves the frog up.
        '''

        theSubObject = self.myBoard.getSubObject(self.frog_id)
        current_x = theSubObject['x']
        current_y = theSubObject['y']
        if current_y != self.y_size-1:
            self.myBoard.editSubObject(self.frog_id, x = current_x, y = current_y+1, direction = "up")

        else: #will change display once frog reaches maximum y
            self.myBoard.editSubObject(self.frog_id, x = current_x, y = self.init_y, direction = "up")
            self.initialize()
            self.displayCount+=1 
            print("Display count: " + str(self.displayCount)) 

        self.frogCheck()

    def frogDown(self):
        '''
        Moves the frog down.
        '''

        theSubObject = self.myBoard.getSubObject(self.frog_id)
        current_x = theSubObject['x']
        current_y = theSubObject['y']
        if current_y != 0:
            self.myBoard.editSubObject(self.frog_id, x = current_x, y = current_y-1, direction = "down")
        self.frogCheck()

    def frogLeft(self):
        '''
        Moves the frog left.
        '''

        theSubObject = self.myBoard.getSubObject(self.frog_id)
        current_x = theSubObject['x']
        current_y = theSubObject['y']
        if current_x != 0:
            self.myBoard.editSubObject(self.frog_id, x = current_x-1, y = current_y, direction = "left")
        self.frogCheck()

    def frogRight(self):
        '''
        Moves the frog right.
        '''

        theSubObject = self.myBoard.getSubObject(self.frog_id)
        current_x = theSubObject['x']
        current_y = theSubObject['y']
        if current_x != self.x_size-1:
            self.myBoard.editSubObject(self.frog_id, x = current_x+1, y = current_y, direction = "right")
        self.frogCheck()

    def getXY(self, x, y):
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

        AtXY = self.myBoard.getXY(x, y)
        if AtXY['segment'] != "" :
            return {
                'segment': AtXY['segment'],
                'type': AtXY['type'],
                'direction': AtXY['direction'],
                'lane': AtXY['lane']
            }
        else:
            return {'lane': AtXY['lane']}       

    def score(self):
        '''
        Returns score as number of display changes
        '''
        return self.displayCount

    #PRIVATE FUNCTIONS
    #No touchy
    def generateBasic(self):
        '''
        Generates a basic game board. This game board has clusters of roads and swamps. Roads and swamps have moving object lanes associated with them.
        '''
        #Some parameters. Since there should be clusters, what shout the minimum and maximum sizes of said clusters be?

        self.currentMinigame = "basic"

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
                "obstacle": Whether or not this is an obstacle that can KILL.
                "platform": Whether or not this is a platform that can SAVE.
            }
        ]
        '''
        availableMOLs = [
            {
                "type": "blueCar",
                "directions": ["left", "right"],
                "visableDirection": True,
                "segments": ['na'],
                "speed": 1,
                "cooldown": 5,
                "lane": "road",
                "obstacle": True,
                "platform": False
            },
            {
                "type": "greenCar",
                "directions": ["left", "right"],
                "visableDirection": True,
                "segments": ['na'],
                "speed": 1,
                "cooldown": 5,
                "lane": "road",
                "obstacle": True,
                "platform": False
            },
            {
                "type": "truck",
                "directions": ["left", "right"],
                "visableDirection": True,
                "segments": ['front', 'middle','back'],
                "speed": 1,
                "cooldown": 3,
                "lane": "road",
                "obstacle": True,
                "platform": False
            },
            {
                "type": "fireTruck",
                "directions": ["left", "right"],
                "visableDirection": True,
                "segments": ['front','back'],
                "speed": 1,
                "cooldown": 4,
                "lane": "road",
                "obstacle": True,
                "platform": False
            },
            {
                "type": "log",
                "directions": ["right"],
                "visableDirection": True,
                "segments": ['front', 'back'],
                "speed": 1,
                "cooldown": 3,
                "lane": "swamp",
                "obstacle": False,
                "platform": True
            }
        ]
        currentlyPlacing = "g" #Stores which cluster we are placing. "g" for grass, "r" for road, "s" for swamp. duh.
        toPlace = random.randrange(GRASS_MIN, GRASS_MAX)
        for y in range(self.y_size):
            if (y == self.y_size-1):
                self.myBoard.setLane(y, "grass")
            elif currentlyPlacing == "g":
                toPlace-=1
                self.myBoard.setLane(y, "grass")
                if toPlace == 0:
                    currentlyPlacing = random.choice(['s', 'r'])
                    if currentlyPlacing == 's':
                        toPlace = random.randrange(SWAMP_MIN, SWAMP_MAX)
                    elif currentlyPlacing == 'r':
                        toPlace = random.randrange(ROAD_MIN, ROAD_MAX)
            elif currentlyPlacing == "s":
                toPlace-=1
                self.myBoard.setLane(y, "swamp")
                self.dangerous_lane.append(y) #Swamps are dangerous
                self.chooseMovingObjectLane(y, "swamp", availableMOLs)
                if toPlace == 0:
                    currentlyPlacing = random.choice(['g', 'r'])
                    if currentlyPlacing == 'g':
                        toPlace = random.randrange(GRASS_MIN, GRASS_MAX)
                    elif currentlyPlacing == 'r':
                        toPlace = random.randrange(ROAD_MIN, ROAD_MAX)
            elif currentlyPlacing == "r":
                toPlace-=1
                self.myBoard.setLane(y, "road")
                self.chooseMovingObjectLane(y, "road", availableMOLs)
                if toPlace == 0:
                    currentlyPlacing = random.choice(['g', 's'])
                    if currentlyPlacing == 'g':
                        toPlace = random.randrange(GRASS_MIN, GRASS_MAX)
                    elif currentlyPlacing == 's':
                        toPlace = random.randrange(SWAMP_MIN, SWAMP_MAX)

    def generateInvaders(self):
        '''
        Generates the space invaders game. The space invaders board is split in half, by a wall. Also, enemies are placed on the board with random velocities. 
        '''
        BACKGROUND = "grass" #The lane for all non-wall areas.
        ENEMY_TYPE = "enemy" #The type for the enemies.
        MAX_ENEMY = 10 #Total number of enemies.
        WALL_TYPE = "wall" #The type for the wall.

        self.currentMinigame = "invaders"

        #Set all lanes to the appropriate lane
        for y in range(self.y_size):
            self.myBoard.setLane(y, BACKGROUND)
        
        #Place wall.
        wallY = math.floor(self.y_size/2) #The y coordinate of the wall. 
        for x in range(self.x_size):
            self.myBoard.addSubObject(self.next_id, WALL_TYPE, x = x, y = wallY)
            self.wall_ids.append(self.next_id)
            self.next_id += 1
        
        #Place enemies.
        numEnemies = random.randrange(1, MAX_ENEMY)
        while numEnemies > 0:
            x = random.randrange(0, self.x_size-1)
            y = random.randrange(wallY+1, self.y_size-1)
            velocity = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
            if self.myBoard.getXY(0,0)['id'] == []:
                self.myBoard.addSubObject(self.next_id, ENEMY_TYPE, x = x, y = y, velocity=velocity)
                self.enemy_ids.append(self.next_id)
                self.next_id+=1
                numEnemies-=1

    def generateMaze(self):
        self.currentMinigame = "lilypads"

    def chooseMovingObjectLane(self, y, laneType, options):
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


        availableMOLs = [i for i in options if i['lane'] == laneType] #All MOLs that fit in with the current laneType
        currentMOL = random.choice(availableMOLs) #The chosen MOL
        random.seed()
        MOLEntry = {
            "y": y,
            "direction": random.choice(currentMOL['directions']),
            "speed": currentMOL['speed'],
            "segments": currentMOL['segments'],
            "type": currentMOL['type'],
            "cooldown": currentMOL['cooldown'],
            "platform": currentMOL['platform'],
            "obstacle": currentMOL['obstacle'],
            "untilNext": random.randrange(1, currentMOL['cooldown']), #Just so that not everything is in sync.
            "entering": False,
            "whichSegment": 0
        }
        self.movingObjectLanes.append(MOLEntry)
        
    def getFrogIntersect(self):
        '''
        @return The list of all things that intersect with the frog
        '''

        frog = self.myBoard.getSubObject(self.frog_id)
        frog_x = frog['x']
        frog_y = frog['y']

        allIDs = self.myBoard.getXY(frog_x, frog_y)['id']
        allIDs.pop(allIDs.index(self.frog_id))
        return allIDs

    def getFrogCollisions(self):
        '''
        @return The list of things that have collided with the frog.
        '''

        allC = self.myBoard.getCollisionsSinceLastUpdate()
        allFrogC = [i for i in allC if self.frog_id in i]
        return allFrogC

    def getInteractions(self):
        '''
        @return A list of all ids that frogger has either collided with or is on top of.
        '''

        interactions = [] #This stores the id of everything that interacts with frogger
        interactions = self.getFrogIntersect() #First we populate it with everything the frog is intersecting.
        collisions = self.getFrogCollisions() #All of the collisions with frogger
        if len(collisions) != 0: #If there is more than one element
            interactions.append(list(self.getFrogCollisions()[0])) #We then append everything that has collided with the frog. Now, we know that this is formatted as a list of tuples, but there should only be one element in this list
        #Otherwise, nothing collides with ya boi frogger
        #interactions = list(dict.fromkeys(interactions)) #Remove duplicates
        return interactions

    def frogCheck(self):
        '''
        Do all checks. Sees if we are dead, and sets the frog's velocity based off of the platform that he is (or isn't) on.
        '''

        dead = False

        #Is ya boi frogger still in the board? Lets see
        try:
            self.myBoard.getSubObject(self.frog_id)
        except:
            self.isDead = True
            print("Frogger sailed off the edge! DEAD")
            return

        #Subobject Testing - Test to see if we have collided with an obstacle
        interactions = self.getInteractions()
        for i in interactions:
            if i in self.obstacle_id:
                print("Frogger hit an obstacle! DEAD")
                dead = True

        
        #Lane testing --Test to see if we are on a dangerous lane. If we are, test to see if we are on a platform. If we are, set froggers velocity to be the velocity of the platform.
        frog_y = self.myBoard.getSubObject(self.frog_id)['y'] #The y coordinate of frogger
        print(frog_y)
        self.myBoard.editSubObject(self.frog_id, velocity=(0,0)) #Pre set the velocity to 0.
        if frog_y in self.dangerous_lane: #If frogger is in a dangerous lane, check if we are on a plaform.
            laneDead = True
            for i in self.platform_id:
                if i in interactions: #If we are standing on a platform...
                    laneDead = False
                    platformVelocity = self.myBoard.getSubObject(i)['velocity'] #Get the velocity of the platform.
                    self.myBoard.editSubObject(self.frog_id, velocity=platformVelocity) #Set our velocity to the velocity of the platform.
                    break
            if laneDead:
                print(f"You are in a killing lane! DEAD Y = {frog_y} Dangerous = {self.dangerous_lane}")
                dead = True
        
        if dead:
            self.isDead = dead

    def updateEnemies(self):
        '''
        Move enemies. Have some of them shoot projectiles. Only for usage in invaders.
        '''

        