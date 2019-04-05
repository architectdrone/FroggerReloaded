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


def text_objects(text, font):
    textSurface = font.render(text, True, color_black)
    return textSurface, textSurface.get_rect()

def game_intro():

    intro = True
    
    frog_rect = frog_image.get_rect()
    frames_per_sec = 100
    fps_clock = pygame.time.Clock()
    
    while intro:        
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(color_white)
        frog_rect = frog_rect.move(speed)
        gameTitle = pygame.font.Font('freesansbold.ttf', 80)
        TextSurf, TextRect = text_objects("Frogger", gameTitle)
        TextRect.center = (400, 200)
        screen.blit(TextSurf, TextRect)

        pygame.draw.rect(screen,color_green,(display_width/6,2*display_height/3,display_width/6,display_height/12))
        pygame.draw.rect(screen,color_red,((4*display_width)/6,2*display_height/3,display_width/6,display_height/12))

        mouse = pygame.mouse.get_pos()
        print(mouse)

        if display_width/3 > mouse[0] > display_width/6 and (2*display_height/3)+(display_height/12) > mouse[1] > 2*display_height/3:
            pygame.draw.rect(screen,color_lightgreen,(display_width/6,2*display_height/3,display_width/6,display_height/12))
        if 5*display_width/6 > mouse[0] > 2*display_width/3 and (2*display_height/3)+(display_height/12) > mouse[1] > 2*display_height/3:
            pygame.draw.rect(screen,color_lightred,((4*display_width)/6,2*display_height/3,display_width/6,display_height/12))

        if(frog_rect.left < 0) or (frog_rect.right >display_width):
            speed[0] =- speed[0]
        if (frog_rect.top < 0) or (frog_rect.bottom > display_height):
            speed[1] =- speed[1]
        screen.blit(frog_image, frog_rect)
        pygame.display.update()
        fps_clock.tick(frames_per_sec)
 

game_intro()
