"""
File: pikaBall.py
Author: Ping
Email: billy3962@hotmail.com
Github: Ping-Lin
Description: ball class, set up the collision and the speed whatever
"""

import pygame
import gbv
import random
import math

class PikaBall(pygame.sprite.Sprite):
    def __init__(self):
        super(PikaBall, self).__init__()

        # ball width and height, and position, and ifstickcollision
        self.width = 95
        self.height = 95
        self.originPos = [None]*2
        self.originPos[0] = (gbv.MARGINLEFT, gbv.BALLHEIGHT)
        self.originPos[1] = (gbv.MARGINRIGHT, gbv.BALLHEIGHT)
        self.ifStickCollision = False
        self.historyPos = [None]*3
        self.historyPosIndex = 0
        self.historyPosIndexDelay = 0   #how many frame need to record one time
        self.ifAttack = False

        # speed and rotate degree
        self.speed = [0, 0]
        self.gravity = gbv.GRAVITY
        self.rotate = 5

        path = 'ball/pikaBall.png'
        self.imageOrigin = loadImg(path, self.width, self.height)
        self.imageHist = loadImg('ball/pikaBall.bmp', self.width, self.height)
        self.image = self.imageOrigin
        self.rect = pygame.Rect(gbv.MARGINLEFT, gbv.BALLHEIGHT,
                                self.width, self.height)

        # add hit picture
        self.ifHitIndex = 0
        self.ifHitPic = False
        self.hitPos = [0, 0]
        self.imageHitPic = loadImg('ball/pa.png', 100, 100)

        # add ball picture
        self.imageShadowPic = loadImg('ball/shadow.bmp', 200, 100)

    def checkMovement(self, clickButton, wallList, pikaList, pos=""):
        """
        check speed and change the speed when collision
        """
        if pos != "":
            self.rect = pygame.Rect(pos[0], pos[1], self.width, self.height)

        self.speed[1] += self.gravity
        # check for collision
        self.speed = self.checkCollision(self.rect, wallList, pikaList, self.speed)
        # check for the max speed

        if pos == "":
            self.rect = self.rect.move(self.speed[0], self.speed[1])

        self.rotate += -1 * self.speed[0]
        self.image = rotateCenter(self.imageOrigin, self.rotate)

    def moveOrigin(self, direction):
        pos = self.originPos[direction]
        self.rect = pygame.Rect(pos[0], pos[1], self.width, self.height)
        self.speed = [0, 0]

    def checkPlace(self):
        """
        check if the ball is out of the window's position
        """
        if self.rect.x > gbv.WINWIDTH or self.rect.x < -self.width or\
           self.rect.y < -self.height or self.rect.y > gbv.WINHEIGHT:
                self.moveOrigin(random.randint(0, 1))

    def update(self, clickButton, wallList, pikaList, pos=""):
        if self.ifHitPic:
            self.ifHitIndex += 1
            if self.ifHitIndex % 5 == 0:
                self.ifHitPic = False
                self.ifHitIndex = 0

        self.checkMovement(clickButton, wallList, pikaList, pos)
        self.checkPlace()
        self.historyPos[self.historyPosIndex] = (self.rect.x, self.rect.y)

        self.historyPosIndexDelay += 1
        if self.historyPosIndexDelay % 3 == 0:
            self.historyPosIndex += 1
        if self.historyPosIndex > 2:
            self.historyPosIndex = 0

    def draw(self, DISPLAYSURF):
        DISPLAYSURF.blit(self.image, self.rect)

    def drawHistory(self, DISPLAYSURF):
        for hist in self.historyPos:
            if hist:
                tmpRect = pygame.Rect(hist[0], hist[1], self.width, self.height)
                DISPLAYSURF.blit(addAlpha(self.imageHist, 100), tmpRect)

    def drawHitPic(self, DISPLAYSURF):
        tmpRect = pygame.Rect(self.hitPos[0], self.hitPos[1], 100, 100)
        DISPLAYSURF.blit(self.imageHitPic, tmpRect)

    def drawShadow(self, DISPLAYSURF):
        shadowSize = int(50 + 40 * (1 - self.rect.y * 1.0 / gbv.WINHEIGHT))
        alpha = int(1 - 1 * (self.rect.y * 1.0 / gbv.WINHEIGHT))
        self.imageShadowPic.set_masks((150, 150, 150, alpha))
        DISPLAYSURF.blit(pygame.transform.scale(self.imageShadowPic,
                         (shadowSize, shadowSize/2)), (self.rect.left, gbv.WINHEIGHT - 70))

    def checkCollision(self, tmpRect, wallList, pikaList, ballSpeed):
        wall = tmpRect.collidelist(wallList)
        pika = tmpRect.collidelist(pikaList)
        # check the wall and stick collision
        if wall == -1 and pika == -1:
            return ballSpeed
        else:
            if wall != 4:
                self.ifStickCollision = False

        if wall == 0:   # left
            return [abs(ballSpeed[0]), ballSpeed[1]]
        elif wall == 1 or tmpRect.centerx >= gbv.WINWIDTH:   # right
            return [-abs(ballSpeed[0]), ballSpeed[1]]
        elif wall == 2 or tmpRect.top <= 0:   # up
            return [ballSpeed[0], abs(ballSpeed[1])]
        elif wall == 3 or tmpRect.bottom >= gbv.WINHEIGHT:   # down
            # set up the hit pic position
            self.ifHitPic = True
            self.hitPos = tmpRect.topleft

            if tmpRect.centerx < gbv.STICKPOS[0]:
                wallList[wall].ifScore = [False, True]
            else:
                wallList[wall].ifScore = [True, False]
            return [ballSpeed[0], -abs(ballSpeed[1])]
        elif wall == 4 and not self.ifStickCollision:   # stick, up and other
            self.ifStickCollision = True
            up = pygame.Rect(gbv.STICKPOS[0]-5, gbv.STICKPOS[1],
                             gbv.STICKWIDTH+10, 5)
            # up
            if tmpRect.colliderect(up):
                return [ballSpeed[0], -abs(ballSpeed[1])]

            # left and right
            if ballSpeed[0] > 0:
                return [-abs(ballSpeed[0]), ballSpeed[1]]
            else:
                return [abs(ballSpeed[0]), ballSpeed[1]]

        # check the pika collision
        if pika != -1:
            dist = abs(pikaList[pika].rect.centerx - tmpRect.centerx)**2+abs(pikaList[pika].rect.centery - tmpRect.centery)**2
            dist = math.sqrt(dist)
            if dist <= 100:
                horizon = (pikaList[pika].rect.centerx-tmpRect.centerx)*(-0.1)
                if pikaList[pika].direct:
                    horizon += 8*random.randrange(5, 11, 1)*0.1
                else:
                    horizon -= 8*random.randrange(5, 11, 1)*0.1

                self.ifAttack = False
                # check if pika is attack or jump or not
                if pikaList[pika].attackingNow:
                    # set up the hit pic position
                    self.ifHitPic = True
                    self.hitPos = tmpRect.midleft

                    # atSpeed = [speed*pikaList[pika].atLevel for speed in pikaList[pika].atSpeed]
                    self.ifAttack = True
                    if pikaList[pika].direct:
                        return pikaList[pika].atSpeed
                    else:
                        return [-pikaList[pika].atSpeed[0], pikaList[pika].atSpeed[1]]
                elif pikaList[pika].jumpingNow:
                    return [horizon, -25]
                else:
                    # check for ball direction
                    return [horizon, -30]

        return ballSpeed

    def getPlace(self):
        """
        for the connect using, because server need to send the message to client
        to get the position
        """
        return (self.rect.x, self.rect.y)


def loadImg(path, width, height):
    """
    load the image, and if the reverse == true then flip
    """
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, (width, height))
    image.set_alpha(10)
    transColor = image.get_at((0, 0))
    image.set_colorkey(transColor)
    return image


def addAlpha(image, alpha):
    newImage = image.convert()
    newImage.set_alpha(alpha)
    return newImage

def rotateCenter(image, angle):
    """rotate an image while keeping its center and size"""
    originRect = image.get_rect()
    rotateImage = pygame.transform.rotate(image, angle)
    rotateRect = originRect.copy()
    rotateRect.center = rotateImage.get_rect().center
    rotateImage = rotateImage.subsurface(rotateRect).copy()
    return rotateImage
