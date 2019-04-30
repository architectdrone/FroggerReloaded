#game logic for Frogger
import board as b
import random
import math
import time
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

        #Control Flow
        self.currentMinigame = "basic" #The minigame we are currently on. Allowed values are "basic", "lilypads", "invaders".
        self.sequence = ["basic", "invaders"]
        self.sequenceIndex = 0
        self.displayCount = 0 #counts change in display

        self.events = [] #For usage with sounds. Basically a list of strings. Please see the getEvents() function for more documentation.
        self.gunCooldown = 0 #How long until the gun can be fired again.
        self.MAX_GUN_COOLDOWN = 3 #Updates between allowed firings.

        self.initialize()

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
        self.enemy_bullet_ids = [] #IDs of things that kill frogger.
        self.frog_bullet_ids  = [] #IDs of things that kill enemies.
        self.movingObjectLanes = [] #Lanes that produce objects. There is a specific internal structure to this list, see chooseMovingObjectLane for deatils
        self.isDead = False #Are we dead?
        self.lilypad_ids = []  # Container for lilypad ID's during Maze Minigame

        self.myBoard = b.Board(self.x_size, self.y_size)
        self.myBoard.addSubObject(self.frog_id, "frog", x = self.init_x, y = self.init_y, direction="up")

        self.generateNext() #Runs the board generator.

    def update(self):
        '''
        -Moves subobjects.
        -Checks if frog is still alive.
        -Move frog if on platform.
        -Move frog out of walls. (For use with the invaders minigame.)
        -Causes new moving objects to enter lanes.
        -If applicable, do checks for enemies.
        '''
        if self.gunCooldown != 0:
            self.gunCooldown-=1

        #Reset events
        self.events = []

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

        #Do an enemy check, and see if we have won.
        self.updateEnemies()
        if self.enemy_ids == []:
                for i in self.wall_ids:
                    self.myBoard.deleteSubObject(i)
                self.wall_ids = []

    def frogUp(self):
        '''
        Moves the frog up.
        '''
        try:
            theSubObject = self.myBoard.getSubObject(self.frog_id)
            current_x = theSubObject['x']
            current_y = theSubObject['y']
            if current_y != self.y_size-1:
                self.myBoard.editSubObject(self.frog_id, x = current_x, y = current_y+1, direction = "up")

            else: #will change display once frog reaches maximum y
                self.myBoard.editSubObject(self.frog_id, x = current_x, y = self.init_y, direction = "up")
                self.initialize()
                self.displayCount+=1 
                #print("Display count: " + str(self.displayCount)) 

            self.frogCheck()
        except:
            self.isDead = True
            self.events.append("death_sailaway")

    def frogDown(self):
        '''
        Moves the frog down.
        '''
        try:
            theSubObject = self.myBoard.getSubObject(self.frog_id)
            current_x = theSubObject['x']
            current_y = theSubObject['y']
            if current_y != 0:
                self.myBoard.editSubObject(self.frog_id, x = current_x, y = current_y-1, direction = "down")
            self.frogCheck()
        except: #If we can't find the frog, that means that we have sailed away.
            self.isDead = True
            self.events.append("death_sailaway")

    def frogLeft(self):
        '''
        Moves the frog left.
        '''
        try:
            theSubObject = self.myBoard.getSubObject(self.frog_id)
            current_x = theSubObject['x']
            current_y = theSubObject['y']
            if current_x != 0:
                self.myBoard.editSubObject(self.frog_id, x = current_x-1, y = current_y, direction = "left")
            self.frogCheck()
        except:
            self.isDead = True
            self.events.append("death_sailaway")

    def frogRight(self):
        '''
        Moves the frog right.
        '''
        try:
            theSubObject = self.myBoard.getSubObject(self.frog_id)
            current_x = theSubObject['x']
            current_y = theSubObject['y']
            if current_x != self.x_size-1:
                self.myBoard.editSubObject(self.frog_id, x = current_x+1, y = current_y, direction = "right")
            self.frogCheck()
        except:
            self.isDead = True
            self.events.append("death_sailaway")

    def frogShoot(self):
        '''
        Shoots a projectile - if we are in the right mode for projectile shooting
        '''
        FROG_BULLET_TYPE = "bubble"
        BULLET_VELOCITY = (0, 2)
        if self.gunCooldown == 0:
            self.myBoard.addSubObject(self.next_id, FROG_BULLET_TYPE, x = self.myBoard.getSubObject(0)['x'], y=self.myBoard.getSubObject(0)['y'], velocity=BULLET_VELOCITY)
            self.frog_bullet_ids.append(self.next_id)
            self.next_id+=1
            self.frogCheck()
            self.gunCooldown = self.MAX_GUN_COOLDOWN

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

    def getEvents(self):
        '''
        Returns a list of events that have happened since the last update. For use in playing sounds.
        -"enemy_shoot": Enemy has shot a bullet.
        -"enemy_dead" : Enemy has been killed.
        -"death_crash": Frog has died b/c something crashed into him.
        -"death_shot" : Frog was shot.
        -"death_swamp": Frog entered a lane that killed him (aka, a swamp)
        -"death_sailaway": Frog sailed off of the edge of the board.
        '''
        return self.events

    #PRIVATE FUNCTIONS
    #No touchy
    def generateNext(self):
        '''
        Generates the next board in the sequence.
        '''
        if self.sequenceIndex == len(self.sequence):
            self.sequenceIndex = 0
        
        #print(self.sequenceIndex)
        nextStage = self.sequence[self.sequenceIndex]
        if nextStage == "basic":
            self.generateBasic()
        elif nextStage == "invaders":
            self.generateInvaders()
        elif nextStage == "maze":
            self.generateMaze() 
        
        self.sequenceIndex+=1

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
        MAX_ENEMY = 5 #Total number of enemies.
        WALL_TYPE = "bush" #The type for the wall.

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
            #Choose available options for velocities
            velocityChoices = []
            if x != self.x_size-1:
                velocityChoices.append((1,0))
            if x != 0:
                velocityChoices.append((-1,0))
            if y != self.y_size-1:
                velocityChoices.append((0,1))
            if y != wallY+1:
                velocityChoices.append((0,-1))

            velocity = random.choice(velocityChoices)
            if self.myBoard.getXY(x,y)['id'] == None:
                self.myBoard.addSubObject(self.next_id, ENEMY_TYPE, x = x, y = y, velocity=velocity)
                self.enemy_ids.append(self.next_id)
                self.next_id+=1
                numEnemies-=1

    def generateMaze(self):
        # declare variables
        SEG_LENGTH_MIN = 2
        SEG_LENGTH_MAX = 3
        x_start = random.randrange(0, self.x_size - 1)
        y_start = 0
        curr_x = x_start
        curr_y = y_start
        orient_option = ['h', 'v']

        # set the type of mini game
        self.currentMinigame = "lilypads"

        # iterate y times
        # set lane's land type
        for y in range(self.y_size - 1):
            # case(s) covered: first lane set grass AND last lane set to grass
            if (y == 0) or (y == (self.y_size - 1)):
                self.myBoard.setLane(y, "grass")
            # case(s) covered: middle lanes set to swamp
            else:
                self.myBoard.setLane(y, "swamp")

        x_start = random.randrange(0, self.x_size - 1)
        y_start = 0
        allSeg = []
        prevSeg = []
        while y < self.y_size:
            seg_len = random.randrange(SEG_LENGTH_MIN, SEG_LENGTH_MAX)
            seg_ori = random.choice(orient_option)

        # x_start = random.randrange(0, size - 1)
        # y_start = 0
        # allSeg = []
        # prevSeg = []
        # LOOP: randomize next segment properties
            #
            # seg_len
            # seg_ori
            # LOOP: decrement seg_len while placing lilypads
            #       along the same orientation for the whole line segment
                # find viable options store in array
                # randomly select option from array
                # place lilypad

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
            self.events.append("death_sailaway")
            print("Frogger sailed off the edge! DEAD")
            return

        #Subobject Testing - Test to see if we have collided with an obstacle or a bullet or a wall
        interactions = self.getInteractions()
        for i in interactions:
            if i in self.obstacle_id:
                print("Frogger hit an obstacle! DEAD")
                self.events.append("death_crash")
                dead = True
            elif i in self.enemy_bullet_ids:
                self.events.append("death_shot")
                print("Frogger got shot! DEAD")
                dead = True
            elif i in self.wall_ids:
                froggerCurrentY = self.myBoard.getSubObject(0)['y']
                self.myBoard.editSubObject(0, y = froggerCurrentY-1)

        #Lane testing --Test to see if we are on a dangerous lane. If we are, test to see if we are on a platform. If we are, set froggers velocity to be the velocity of the platform.
        frog_y = self.myBoard.getSubObject(self.frog_id)['y'] #The y coordinate of frogger
        frog_x = self.myBoard.getSubObject(self.frog_id)['x'] #The x coordinate of frogger
        self.myBoard.editSubObject(self.frog_id, velocity=(0,0)) #Pre set the velocity to 0.
        if frog_y in self.dangerous_lane: #If frogger is in a dangerous lane, check if we are on a plaform.
            laneDead = True
            for i in self.platform_id:
                if i in interactions: #If we are standing on a platform...
                    #Basic Collisions
                    laneDead = False
                    platformVelocity = self.myBoard.getSubObject(i)['velocity'] #Get the velocity of the platform.
                    self.myBoard.editSubObject(self.frog_id, velocity=platformVelocity) #Set our velocity to the velocity of the platform.
                    break
            if laneDead:
                for i in self.platform_id:
                    try:
                        if frog_x == self.myBoard.getSubObject(i)['x']-1 and frog_y == self.myBoard.getSubObject(i)['y']:
                            laneDead = False
                            platformVelocity = self.myBoard.getSubObject(i)['velocity'] #Get the velocity of the platform.
                            platform_back_x = self.myBoard.getSubObject(i)['x']
                            platform_back_y = self.myBoard.getSubObject(i)['y']
                            self.myBoard.editSubObject(self.frog_id, x=platform_back_x, y=platform_back_y, velocity=platformVelocity) #Set our velocity to the velocity of the platform.
                            break
                    except:
                        continue
                
            
            if laneDead:
                #Saving Grace Rule - If off by one, put him on the back of the log.                    
                self.events.append("death_swamp")
                print(f"You are in a killing lane! DEAD Y = {frog_y} Dangerous = {self.dangerous_lane}")
                dead = True
        
        if dead:
            self.isDead = dead

    def updateEnemies(self):
        '''
        Move enemies. Have some of them shoot projectiles. Check if enemies have died. Only for usage in invaders.
        '''
        FIRING_CHANCE = 0.4 #Chance of a given enemy firing.
        MAX_SHOOTERS = 4 #Maximum amount of enemies that can fire in a given tick.
        BULLET_VELOCITY = (0, -1) #Velocity of a bullet. Make sure the Y coordinate is negative!
        BULLET_TYPE = "enemyProjectile"

        current_shooters = MAX_SHOOTERS
        enemyCollisions = []
        for i in self.enemy_ids:
            #Update positions of enemies.
            theSubObject = self.myBoard.getSubObject(i)
            x = theSubObject['x']
            y = theSubObject['y']
            new_velocity = theSubObject['velocity']
            if x == 0 and theSubObject['velocity'] == (-1,0):
                new_velocity = (1,0)
            elif x == self.x_size-1 and theSubObject['velocity'] == (1,0):
                new_velocity = (-1,0)
            elif y <= math.floor(self.y_size/2)+1 and theSubObject['velocity'] == (0,-1):
                new_velocity = (0,1)
            elif y == self.y_size-1 and theSubObject['velocity'] == (0,1):
                new_velocity = (0,-1)

            self.myBoard.editSubObject(i, velocity=new_velocity)

            #Fire, potentially.
            if random.randrange(1, 100) < FIRING_CHANCE*100:
                if current_shooters > 0:
                    if "enemy_shoot" not in self.events:
                        self.events.append("enemy_shoot")
                    self.myBoard.addSubObject(self.next_id, BULLET_TYPE, x = x, y = y, velocity=BULLET_VELOCITY)
                    self.enemy_bullet_ids.append(self.next_id)
                    self.next_id+=1
                    current_shooters-=1

            #Get collisions with this enemy.
            for c in self.myBoard.getCollisionsSinceLastUpdate():
                if i in c:
                    enemyCollisions.append(c)
        #Check to see if enemy is dead
        for collision in enemyCollisions:
            for subObjectID in collision:
                if subObjectID in self.frog_bullet_ids:
                    try:
                        self.events.append("enemy_dead")
                        self.frog_bullet_ids.remove(subObjectID) #Destroy Bullet
                        enemy_id = 0
                        if collision[0] != subObjectID:
                            enemy_id = collision[0]
                        else:
                            enemy_id = collision[1]
                        self.enemy_ids.remove(enemy_id) #Destroy Enemy
                        self.myBoard.deleteSubObject(enemy_id)
                        self.myBoard.deleteSubObject(subObjectID)
                    except:
                        continue
