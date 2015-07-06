"""
File: mainScreen.py
Author: Ping
Email: billy3962@hotmail.com
Github: Ping-Lin
Description: show the main game screen and the game process
"""

import pygame
import sys
from pygame.locals import *
import gbv
import character.pika

def runGame(pikaGroup):
    """
    Run the main loop of game
    """
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.quit()

        # draw the image
        pikaGroup.update()
        DISPLAYSURF.fill(gbv.BGCOLOR)
        pikaGroup.draw(DISPLAYSURF)
        pygame.display.update()
        pygame.time.Clock().tick(30)

def main():
    global IMAGE, DISPLAYSURF
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((gbv.WINWIDTH, gbv.WINHEIGHT))
    pygame.display.set_caption('PikaBall X Connect')

    # Load the element
    pikaLeft = character.pika.Pika()
    pikaGroup = pygame.sprite.Group(pikaLeft)

    while True:
        runGame(pikaGroup)

if __name__ == '__main__':
    main()

