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

        # Load the pika image: walk, pu, jump
        self.pikaImages = []
        for i in xrange(1, 6):
            path = 'character/pikaToRight' + str(i) + '.bmp'
            self.pikaImages.append(
                loadImage(path, reverse, self.width, self.height))

        self.pikaPuImages = []
        for i in xrange(1, 6):
            j = 3 if i >= 4 else i
            path = 'character/pikaPu' + str(j) + '.bmp'
            self.pikaPuImages.append(
                loadImage(path, False, self.width, self.height))
        for i in xrange(1, 6):
            j = 3 if i >= 4 else i
            path = 'character/pikaPu' + str(j) + '.bmp'
            self.pikaPuImages.append(
                loadImage(path, True, self.width, self.height))

        # direction and motion
        self.direct = reverse
        self.jump = False
        self.jumpingNow = False
        self.pu = False
        self.puingNow = False
        self.attack = False
        self.attackingNow = False

        # speed, gravity and height
        self.speed = [0, 0]
        self.gravity = gbv.GRAVITY
        self.pikaHeight = 250
        self.pikaV0 = -27

        # initialize the image and rect
        self.index = 0
        self.indexPu = 0
        self.indexAt = 0
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
                self.attack = self.pu = True
        else:
            if clickButton['a']:
                self.speed[0] -= 10
            if clickButton['d']:
                self.speed[0] += 10
            if clickButton['w']:
                self.jump = True
            if clickButton['lshift']:
                self.attack = self.pu = True

        # jumping or not
        if self.jump and not self.jumpingNow and not self.puingNow:
            self.speed[1] = self.pikaV0
            self.jumpingNow = True
        if self.jumpingNow:
            self.speed[1] += self.gravity
        if self.rect.y + self.speed[1] >= gbv.MARGINHEIGHT:
            self.speed[1] = gbv.MARGINHEIGHT - self.rect.y
            self.jumpingNow = False

        if self.pu and not self.puingNow and not self.jumpingNow:
            self.indexPu = 0
            self.puingNow = True
        if self.puingNow:
            self.indexPu += 1
            index = self.indexPu / 3
            if index == 4:
                self.puingNow = False
            if self.direct and not clickButton["a"] or clickButton["right"]:
                self.image = self.pikaPuImages[index]
                self.speed[0] = 14 if index % 5 <= 2 else 0
            else:
                self.image = self.pikaPuImages[index + 5]
                self.speed[0] = -14 if index % 5 <= 2 else 0

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
        self.pu = False
        self.attack = False

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
