import pygame 
from pygame.locals import *
import sys

pygame.init()
speed = [1, 1]
color_white = (255,255,255)
color_black = (0,0,0)
window_size = (width, height) = (800,600)
pygame.display.set_caption('Frogger Reloaded')
frog_image = pygame.image.load('frog.jpg')

screen = pygame.display.set_mode(window_size)

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
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(color_white)
        frog_rect = frog_rect.move(speed)
        gameTitle = pygame.font.Font('freesansbold.ttf', 60)
        TextSurf, TextRect = text_objects("Frogger", gameTitle)
        TextRect.center = (400, 200)
        screen.blit(TextSurf, TextRect)

        if(frog_rect.left < 0) or (frog_rect.right > width):
            speed[0] =- speed[0]
        if (frog_rect.top < 0) or (frog_rect.bottom > height):
            speed[1] =- speed[1]
        screen.blit(frog_image, frog_rect)
        pygame.display.update()
        fps_clock.tick(frames_per_sec)
 

game_intro()
