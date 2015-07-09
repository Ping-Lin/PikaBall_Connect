"""
File: pika.py
Author: Ping
Email: billy3962@hotmail.com
Github: Ping-Lin
Description: pika.py store the information of the pika character
"""
import pygame
from pygame.locals import *
import gbv


class Pika(pygame.sprite.Sprite):
    def __init__(self, reverse=False):
        super(Pika, self).__init__()

        # pika width and height
        self.width = 128
        self.height = 128

        # Load the pika image
        self.pikaImages = []
        for i in xrange(1, 6):
            path = 'character/pikaToRight' + str(i) + '.bmp'
            self.pikaImages.append(
                loadImage(path, reverse, self.width, self.height))

        # direction
        self.direct = reverse
        self.jump = False
        self.jumpingNow = False

        # speed, gravity and height
        self.speed = [0, 0]
        self.gravity = gbv.GRAVITY
        self.pikaHeight = 250
        self.pikaV0 = -27

        # initialize the image and rect
        self.index = 0
        self.image = self.pikaImages[self.index]
        if reverse is False:
            self.rect = pygame.Rect(
                gbv.MARGINRIGHT, gbv.MARGINHEIGHT, self.width, self.height)
        else:
            self.rect = pygame.Rect(
                gbv.MARGINLEFT, gbv.MARGINHEIGHT, self.width, self.height)

    def checkMovement(self, clickButton, wallList):
        """
        check speed and add the speed to the movement
        """
        self.speed[0] = 0
        if self.jumpingNow is False:
            self.speed[1] = 0

        if not self.direct:
            if clickButton['left']:
                self.speed[0] -= 10
            if clickButton['right']:
                self.speed[0] += 10
            if clickButton['up']:
                self.jump = True
            if clickButton['space']:
                self.attack = True
        else:
            if clickButton['a']:
                self.speed[0] -= 10
            if clickButton['d']:
                self.speed[0] += 10
            if clickButton['w']:
                self.jump = True
            if clickButton['lctrl']:
                self.attack = True

        if self.jump and not self.jumpingNow:
            self.speed[1] = self.pikaV0
            self.jumpingNow = True

        if self.jumpingNow:
            self.speed[1] += self.gravity
        if self.rect.y + self.speed[1] >= gbv.MARGINHEIGHT:
            self.speed[1] = gbv.MARGINHEIGHT - self.rect.y
            self.jumpingNow = False

        # check for collision
        tmpRect = self.rect.move(self.speed[0], self.speed[1])
        if checkCollision(tmpRect, wallList):
            self.rect = self.rect.move(0, self.speed[1])
        else:
            self.rect = tmpRect

    def update(self, clickButton, wallList):
        """
        something initialization and every update
        contain the image change, and the attack initialization
        """
        self.attack = False
        self.jump = False

        self.index += 1
        index = self.index/5
        if index >= len(self.pikaImages):
            self.index = 0
            index = 0
        self.image = self.pikaImages[index]
        # check movement
        self.checkMovement(clickButton, wallList)


def loadImage(path, reverse, width, height):
    """
    load the image, and if the reverse == true then flip
    """
    image = pygame.image.load(path).convert()
    image = pygame.transform.flip(image, reverse, False)
    image = pygame.transform.scale(image, (width, height))
    transColor = image.get_at((0, 0))
    image.set_colorkey(transColor)
    return image


def checkCollision(tmpRect, wallList):
    if tmpRect.collidelist(wallList) == -1:
        return False
    else:
        return True
