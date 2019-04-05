import pygame 
from pygame.locals import *
import sys

pygame.init()
speed = [1, 1]
display_width = 800
display_height = 600

color_white = (255,255,255)
color_black = (0,0,0)
color_red = (200,0,0)
color_green = (0,200,0) 

color_lightred = (255,0,0)
color_lightgreen = (0,255,0)

pygame.display.set_caption('Frogger Reloaded')
frog_image = pygame.image.load('frog.jpg')

screen = pygame.display.set_mode((display_width, display_height))

gameTitle = pygame.font.Font('freesansbold.ttf', 80)
smallText = pygame.font.Font('freesansbold.ttf', 30)


def text_objects(text, font):
    textSurface = font.render(text, True, color_black)
    return textSurface, textSurface.get_rect()

def game_button(msg,x,y,w,h,c,l,action=None):
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

def game_quit():
    pygame.quit()
    quit()

def game_intro():

    intro = True
    
    frog_rect = frog_image.get_rect()
    frames_per_sec = 100
    fps_clock = pygame.time.Clock()
    
    while intro:        
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(color_white)
        TextSurf, TextRect = text_objects("Frogger", gameTitle)
        TextRect.center = (400, 200)
        screen.blit(TextSurf, TextRect)

        game_button("Start!",display_width/6,2*display_height/3,display_width/6,display_height/12,color_green,color_lightgreen,None)
        game_button("Quit", 2*display_width/3,2*display_height/3,display_width/6,display_height/12,color_red,color_lightred,game_quit)

        frog_rect = frog_rect.move(speed)
        if(frog_rect.left < 0) or (frog_rect.right >display_width):
            speed[0] =- speed[0]
        if (frog_rect.top < 0) or (frog_rect.bottom > display_height):
            speed[1] =- speed[1]
        screen.blit(frog_image, frog_rect)
        pygame.display.update()
        fps_clock.tick(frames_per_sec)
 
 #def game_play():


game_intro()
