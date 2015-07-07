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
from obstacle.wall import Wall

def runGame(spriteGroup, wallList):
    """
    Run the main loop of game
    """
    clickButton = dict.fromkeys(
        ['left', 'right', 'up', 'space',
         'a', 'd', 'w', 'lctrl'])
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    clickButton['left'] = True
                elif event.key == pygame.K_RIGHT:
                    clickButton['right'] = True
                elif event.key == pygame.K_UP:
                    clickButton['up'] = True
                elif event.key == pygame.K_SPACE:
                    clickButton['space'] = True
                elif event.key == pygame.K_a:
                    clickButton['a'] = True
                elif event.key == pygame.K_d:
                    clickButton['d'] = True
                elif event.key == pygame.K_w:
                    clickButton['w'] = True
                elif event.key == pygame.K_LCTRL:
                    clickButton['lctrl'] = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    clickButton['left'] = False
                elif event.key == pygame.K_RIGHT:
                    clickButton['right'] = False
                elif event.key == pygame.K_UP:
                    clickButton['up'] = False
                elif event.key == pygame.K_SPACE:
                    clickButton['space'] = False
                elif event.key == pygame.K_a:
                    clickButton['a'] = False
                elif event.key == pygame.K_d:
                    clickButton['d'] = False
                elif event.key == pygame.K_w:
                    clickButton['w'] = False
                elif event.key == pygame.K_LCTRL:
                    clickButton['lctrl'] = False

        # draw the image
        DISPLAYSURF.fill(gbv.BGCOLOR)
        spriteGroup.update(clickButton, wallList)
        spriteGroup.draw(DISPLAYSURF)
        pygame.display.update()
        CLOCK.tick(15)


def main():
    global IMAGE, DISPLAYSURF, CLOCK
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((gbv.WINWIDTH, gbv.WINHEIGHT))
    pygame.display.set_caption('PikaBall X Connect')
    CLOCK = pygame.time.Clock()

    # Load the element
    pikaLeft = character.pika.Pika(True)
    pikaRight = character.pika.Pika()
    spriteGroup = pygame.sprite.Group(pikaLeft)
    spriteGroup.add(pikaRight)
    wallList = []
    wallList.append(
        Wall(pygame.Rect(gbv.WINWIDTH-pikaLeft.width*0.7, 0, 1, gbv.WINHEIGHT)))
    wallList.append(
        Wall(pygame.Rect(0, 0, 1, gbv.WINHEIGHT)))
    wallList.append(
        Wall(pygame.Rect(0, 0, gbv.WINWIDTH, 1)))
    wallList.append(
        Wall(pygame.Rect(
            gbv.STICKPOS[0], gbv.STICKPOS[1], gbv.STICKWIDTH, gbv.STICKHEIGHT),
            img=True))
    spriteGroup.add(wallList[-1])   # add the stick

    while True:
        runGame(spriteGroup, wallList)

if __name__ == '__main__':
    main()
