# Pygame implementation for FroggerReloaded
import pygame 
from pygame.locals import *
import sys
import time
import gamelogic
import highScores

pygame.init()
X_SIZE = 15
Y_SIZE = 10
sprite_size = 50
display_width = X_SIZE*sprite_size
display_height = Y_SIZE*sprite_size

#Game sound
pygame.mixer.init(23433,16,2,4096)
buttonclick = pygame.mixer.Sound("music/clickbutton.wav")
soundB = pygame.mixer.Channel(2)
drawning = pygame.mixer.Sound("music/drawning.wav")
crash = pygame.mixer.Sound("music/crash.wav")
bullethit = pygame.mixer.Sound("music/bullethit.wav")


#Game Speed
betweenUpdates = 15
msBetweenInputs = 20 #Number of MS before an input is repeated.
pygame.key.set_repeat(0, msBetweenInputs)

#Colors
color_white = (255,255,255)
color_black = (0,0,0)
color_gray = (125,125,125)
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
bubble = pygame.image.load('SPRITES/bubble.png')
enemy = pygame.image.load('SPRITES/enemy.png')
turtlePad = pygame.image.load('SPRITES/turtle_pad.png')
enemyProjectile = pygame.image.load('SPRITES/enemy_projectile.png')
gameover_image = pygame.image.load('over.png')
background_image = pygame.transform.scale(background_image,(display_width,display_height))
gameover_image = pygame.transform.scale(gameover_image,(display_width,display_height))
grass_image = pygame.transform.scale(grass_image,(sprite_size,sprite_size))
road_image = pygame.transform.scale(road_image,(sprite_size,sprite_size))
water_image = pygame.transform.scale(water_image,(sprite_size,sprite_size))
frog_na_down = pygame.transform.scale(frog_na_down,(sprite_size,sprite_size))
frog_na_up = pygame.transform.scale(frog_na_up,(sprite_size,sprite_size))
frog_na_left = pygame.transform.scale(frog_na_left,(sprite_size,sprite_size))
frog_na_right = pygame.transform.scale(frog_na_right,(sprite_size,sprite_size))
blueCar_na_right = pygame.transform.scale(blueCar_na_right,(sprite_size,sprite_size))
blueCar_na_left = pygame.transform.scale(blueCar_na_left,(sprite_size,sprite_size))
greenCar_na_right = pygame.transform.scale(greenCar_na_right,(sprite_size,sprite_size))
greenCar_na_left = pygame.transform.scale(greenCar_na_left,(sprite_size,sprite_size))
truck_front_right = pygame.transform.scale(truck_front_right,(sprite_size,sprite_size))
truck_middle_right = pygame.transform.scale(truck_middle_right,(sprite_size,sprite_size))
truck_back_right = pygame.transform.scale(truck_back_right,(sprite_size,sprite_size))
truck_front_left = pygame.transform.scale(truck_front_left,(sprite_size,sprite_size))
truck_middle_left = pygame.transform.scale(truck_back_left,(sprite_size,sprite_size))
truck_back_left = pygame.transform.scale(truck_back_left,(sprite_size,sprite_size))
firetruck_front_right = pygame.transform.scale(firetruck_front_right,(sprite_size,sprite_size))
firetruck_back_right = pygame.transform.scale(firetruck_back_right,(sprite_size,sprite_size))
firetruck_front_left = pygame.transform.scale(firetruck_front_left,(sprite_size,sprite_size))
firetruck_back_left = pygame.transform.scale(firetruck_back_left,(sprite_size,sprite_size))
log_front_right = pygame.transform.scale(log_front_right,(sprite_size,sprite_size))
log_back_right = pygame.transform.scale(log_back_right,(sprite_size,sprite_size))
bubble = pygame.transform.scale(bubble,(sprite_size,sprite_size))
enemy = pygame.transform.scale(enemy,(sprite_size,sprite_size))
turtlePad = pygame.transform.scale(turtlePad,(sprite_size,sprite_size))
enemyProjectile = pygame.transform.scale(enemyProjectile,(sprite_size,sprite_size))

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
    'log_back_right': log_back_right,
    'bubble_na_na' : bubble,
    'enemy_na_na' : enemy,
    'turtlePad_na_na' : turtlePad,
    'enemyProjectile_na_na' : enemyProjectile
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


    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen,l,(x,y,w,h))
        if click[0] == 1 and action != None:
            buttonclick.play()
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

    #Play menu background music
    pygame.mixer.music.stop()
    pygame.mixer.music.load("music/menu.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1) #loop it

    frog_rect = frog_image.get_rect()
    frames_per_sec = 100
    #fps_clock = pygame.time.Clock()
    
    while intro:        
        for event in pygame.event.get():
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

        pygame.display.update()
        fps_clock.tick(frames_per_sec)

#Game Frame Helper Functions
def display(g):
    '''
    Update the window according to what gamelogic tells us.
    @param g The game object to display for.
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
            
            newImages = []
            if segments is not None:
                for i in range(len(segments)):
                    newImages.append(getSprite(types[i], segments[i], directions[i]))
                newImages = newImages[::-1] #Reverse the list. TODO actually add precedance.
            
            imagesToDisplay+=newImages
            for i in imagesToDisplay:
                drawSprite(i, tile_x, tile_y)
            
def drawSprite(image,tile_x,tile_y):
    screen.blit(image,(tile_x*sprite_size,(Y_SIZE-tile_y-
    1)*sprite_size))

# Responsible for displaying the score in the corner of the screen
def drawScore(score):
    scoreFont = pygame.font.SysFont('Comic Sans MS', 30)
    textScore = scoreFont.render(str (score), False, color_white)
    screen.blit(textScore, (display_width-40, display_height-40))
           
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

    #Play background music
    pygame.mixer.music.stop()
    pygame.mixer.music.load("music/game.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1) #loop it
    '''
    The game frame itself
    '''
    global betweenUpdates

    run = True
    g = gamelogic.game(X_SIZE, Y_SIZE)    
    nextCommand = ""
    updateCounter = betweenUpdates
    score = 0

    while run:
        '''
        clockobject = pygame.time.Clock()
        clockobject.tick(60)
        '''

        #Get events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #Reset the screen
        screen.fill(color_black)

        #Update the game frame
        display(g) 

        #Increment score
        score += 1

        #Display score
        drawScore(g.score())

        #Handle keypresses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            nextCommand = "up"
        elif keys[pygame.K_DOWN]:
            nextCommand = "down"
        elif keys[pygame.K_LEFT]:
            nextCommand = "left"
        elif keys[pygame.K_RIGHT]:
            nextCommand = "right"
        elif keys[pygame.K_SPACE]:
            nextCommand = "launch"
        if keys[pygame.K_ESCAPE]:
                run = False

        #Update, if needed
        
        if updateCounter == 0:

            g.update()
            #Play sounds
            event = g.getEvents()
            if 'death_sailaway' in event:
                drawning.play()
            if 'death_crash' in event:
                crash.play()
            if 'death_shot' in event:
                bullethit.play()
            if 'death_swamp' in event:
                drawning.play()
            if 'enemy_dead' in event:
                bullethit.play()
            if 'enemy_shoot' in event:
                buttonclick.play()

            if nextCommand == "up":
                g.frogUp()
            if nextCommand == "down":
                g.frogDown()
            if nextCommand == "left":
                g.frogLeft()
            if nextCommand == "right":
                g.frogRight()
            if nextCommand == "launch":
                g.frogShoot()
            nextCommand = ""

            
            updateCounter = betweenUpdates
        
        #Are we dead?
        if g.isDead:
            #Do something, I guess? idk lol
            run = False
            
            
            #add name and score to file after game over
            userScore = g.score()
            highest = highScores.findHighestScore("highscores.txt")
            if (userScore > highest):
                print('Congradulations, you have the highest score')
                userName = input("What is your name? ")
                assert userName is not None
                highScores.writeToFile("highscores.txt", userName, userScore)
        
            #display top scores <=10
            highScores.displayScores("highscores.txt" , 10)

            gameOver()
            
            
        #Update the screen using pygame methods
        pygame.display.update()

        updateCounter-=1



#Generl Helper Functions
def gameOver():

    #Game over background music
    pygame.mixer.music.stop()
    pygame.mixer.music.load("music/gameover.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1) #loop it
    
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #screen.fill(color_red)
        screen.blit(gameover_image, [0,0])
        game_button("Restart!",3*display_width/12,8*display_height/9,display_width/6,display_height/12,color_red,color_lightgreen,game_intro)
        game_button("Quit!",7*display_width/12,8*display_height/9,display_width/6,display_height/12,color_red,color_gray,game_quit)

        #TextSurf, TextRect = text_objects("RIP", gameTitle)
        #TextRect.center = (display_width/2, display_height/3)
        #TextSurf1, TextRect1 = text_objects("SPACE TO QUIT", smallText)
        #TextRect1.center = (display_width/2, 400)
        #screen.blit(TextSurf, TextRect)
        #screen.blit(TextSurf1, TextRect1)

        #keys = pygame.key.get_pressed()
        #if keys[pygame.K_SPACE]:
        #    game_quit()

        pygame.display.update()
    



def game_quit(): 
    '''
    Quits the game
    '''
    pygame.quit()
    quit()
 
#Begin the game
if __name__ == '__main__':
    game_intro()


