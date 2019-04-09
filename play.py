import pygame 
from pygame.locals import *
import sys
import time
import gamelogic as g

pygame.init()
speed = [1, 1]
X_SIZE = 9
Y_SIZE = 6
display_width = X_SIZE*79
display_height = Y_SIZE*79

#Game Speed
betweenUpdates = 30

#Colors
color_white = (255,255,255)
color_black = (0,0,0)
color_red = (200,0,0)
color_green = (0,200,0) 
color_lightred = (255,0,0)
color_lightgreen = (0,255,0)

#Load images
pygame.display.set_caption('Frogger Reloaded')
frog_image = pygame.image.load('frog.png')
background_image = pygame.image.load("s2.jpg")
grass_image = pygame.image.load('SPRITES/grass.png')
road_image = pygame.image.load('SPRITES/road.png')
water_image = pygame.image.load('SPRITES/water.png')
frog_na_down = pygame.image.load('SPRITES/frog_na_down.png')
frog_na_up = pygame.image.load('SPRITES/frog_na_up.png')
frog_na_left = pygame.image.load('SPRITES/frog_na_left.png')
frog_na_right = pygame.image.load('SPRITES/frog_na_right.png')
blueCar_na_right = pygame.image.load('SPRITES/blueCar_na_right.png')
blueCar_na_left = pygame.image.load('SPRITES/blueCar_na_left.png')
greenCar_na_right = pygame.image.load('SPRITES/greenCar_na_right.png')
greenCar_na_left = pygame.image.load('SPRITES/greenCar_na_left.png')
truck_front_right = pygame.image.load('SPRITES/truck_front_right.png')
truck_middle_right = pygame.image.load('SPRITES/truck_middle_right.png')
truck_back_right = pygame.image.load('SPRITES/truck_back_right.png')
truck_front_left = pygame.image.load('SPRITES/truck_front_left.png')
truck_middle_left = pygame.image.load('SPRITES/truck_middle_left.png')
truck_back_left = pygame.image.load('SPRITES/truck_back_left.png')
firetruck_front_right = pygame.image.load('SPRITES/firetruck_front_right.png')
firetruck_back_right = pygame.image.load('SPRITES/firetruck_back_right.png')
firetruck_front_left = pygame.image.load('SPRITES/firetruck_front_left.png')
firetruck_back_left = pygame.image.load('SPRITES/firetruck_back_left.png')
log_front_right = pygame.image.load('SPRITES/log_front_right.png')
log_back_right = pygame.image.load('SPRITES/log_back_right.png')

imageDict = {
    'frog_na_down': frog_na_down,
    'frog_na_up': frog_na_up,
    'frog_na_left': frog_na_left,
    'frog_na_right': frog_na_right,
    'blueCar_na_right': blueCar_na_right,
    'blueCar_na_left': blueCar_na_left,
    'greenCar_na_right': greenCar_na_right,
    'greenCar_na_left': greenCar_na_left,
    'truck_front_right': truck_front_right,
    'truck_middle_right': truck_middle_right,
    'truck_back_right': truck_back_right,
    'truck_front_left': truck_front_left,
    'truck_middle_left': truck_middle_left,
    'truck_back_left': truck_back_left,
    'fireTruck_front_right': firetruck_front_right,
    'fireTruck_back_right': firetruck_back_right,
    'fireTruck_front_left': firetruck_front_left,
    'fireTruck_back_left': firetruck_back_left,
    'log_front_right': log_front_right,
    'log_back_right': log_back_right
}

#Makes the screen
screen = pygame.display.set_mode((display_width, display_height))

#Sets the fonts for the menu
gameTitle = pygame.font.Font('freesansbold.ttf', 80)
smallText = pygame.font.Font('freesansbold.ttf', 30)

#Initializes the clock
fps_clock = pygame.time.Clock()

#HELPER FUNCTIONS
#Menu Helper Functions
def text_objects(text, font):
    '''
    @return A text object
    '''
    textSurface = font.render(text, True, color_black)
    return textSurface, textSurface.get_rect()

def game_button(msg,x,y,w,h,c,l,action=None):
    '''
    Display a button to the screen
    @param msg The message to print
    @param x The x coordinate
    @param y The y coordinate
    @param w The width
    @param h The height
    @param c The color of the button
    @param l The color after hovering
    @param action A function to be execute upon pressing the button
    '''
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(mouse)

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen,l,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen,c,(x,y,w,h))

    buttonSurf, buttonRect = text_objects(msg, smallText)
    buttonRect.center = (x+w/2, y+h/2)
    screen.blit(buttonSurf, buttonRect)

def game_intro():
    '''
    Shows the initial game menu
    '''
    intro = True
    
    frog_rect = frog_image.get_rect()
    frames_per_sec = 100
    #fps_clock = pygame.time.Clock()
    
    while intro:        
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #screen.fill(color_white)
        screen.blit(background_image, [0,0])
        TextSurf, TextRect = text_objects("Frogger", gameTitle)
        TextRect.center = (400, 200)
        screen.blit(TextSurf, TextRect)

        game_button("Start!",display_width/6,2*display_height/3,display_width/6,display_height/12,color_green,color_lightgreen,game_play)
        game_button("Quit", 2*display_width/3,2*display_height/3,display_width/6,display_height/12,color_red,color_lightred,game_quit)

        frog_rect = frog_rect.move(speed)
        if(frog_rect.left < 0) or (frog_rect.right >display_width):
            speed[0] =- speed[0]
        if (frog_rect.top < 0) or (frog_rect.bottom > display_height/2):
            speed[1] =- speed[1]
        screen.blit(frog_image, frog_rect)
        pygame.display.update()
        fps_clock.tick(frames_per_sec)

#Game Frame Helper Functions
def display():
    '''
    Update the window according to what gamelogic tells us.
    '''
    #TODO define X_SIZE and Y_SIZE
    for tile_x in range(X_SIZE):
        for tile_y in range(Y_SIZE):
            atXY = g.getXY(tile_x, tile_y)

            segments = atXY['segment']
            types = atXY['type']
            directions = atXY['direction']
            lane = atXY['lane']

            imagesToDisplay = []
            if lane == 'grass':
                imagesToDisplay.append(grass_image)
            elif lane == 'road':
                imagesToDisplay.append(road_image)
            if lane == 'swamp': #Make sure this is right...
                imagesToDisplay.append(water_image)
            
            if segments is not None:
                for i in range(len(segments)-1):
                    imagesToDisplay.append(getSprite(types[i], segments[i], directions[i]))
            
            for i in imagesToDisplay:
                drawSprite(i, tile_x, tile_y)
        
def drawSprite(image,tile_x,tile_y):
    screen.blit(image,(tile_x*79,(Y_SIZE-tile_y)*79))
           
# Retrieves images based on given properties
def getSprite(type, seg, dir):

    '''
    Get the image associated with the parameters
    @param type The type of the sprite.
    @param seg The segment of the image (can be front, middle, back, or na)
    @param dir The direction of the image (can be left, right, na)
    '''
    global imageDict
    image = imageDict[type+'_'+seg+'_'+dir]
    return image

def game_play():
    '''
    The game frame itself
    '''
    global betweenUpdates

    run = True
    g.initialize() #Create the game board
    updateCounter = betweenUpdates

    while run:
        #Get events
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #Reset the screen
        screen.fill(color_black)

        #Update the game frame
        display() 

        #Handle keypresses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            g.frogUp()
        elif keys[pygame.K_DOWN]:
            g.frogDown()
        elif keys[pygame.K_LEFT]:
            g.frogLeft()
        elif keys[pygame.K_RIGHT]:
            g.frogRight()
        if keys[pygame.K_ESCAPE]:
            run = False

        #Update, if needed
        updateCounter-=1
        if updateCounter == 0:
            g.update()
            updateCounter = betweenUpdates
        
        #Are we dead?
        if g.isDead:
            #Do something, I guess? idk lol
            game_quit()
            
        #Update the screen using pygame methods
        pygame.display.update()

#Generl Helper Functions
def game_quit(): 
    '''
    Quits the game
    '''
    pygame.quit()
    quit()
 
#Begin the game
game_intro()


