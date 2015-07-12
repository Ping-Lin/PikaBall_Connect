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

class PikaBall(pygame.sprite.Sprite):
    def __init__(self):
        super(PikaBall, self).__init__()

        # ball width and height, and position, and ifstickcollision
        self.width = 100
        self.height = 100
        self.originPos = [None]*2
        self.originPos[0] = (gbv.MARGINLEFT, gbv.BALLHEIGHT)
        self.originPos[1] = (gbv.MARGINRIGHT, gbv.BALLHEIGHT)
        self.ifStickCollision = False

        # speed and rotate degree
        self.speed = [0, 0]
        self.gravity = gbv.GRAVITY
        self.rotate = 10

        path = 'ball/pikaBall.bmp'
        self.imageOrigin = loadImg(path, self.width, self.height)
        self.image = self.imageOrigin
        self.rect = pygame.Rect(gbv.MARGINLEFT, gbv.BALLHEIGHT,
                                self.width, self.height)

    def checkMovement(self, clickButton, wallList, pikaList):
        """
        check speed and change the speed when collision
        """
        self.speed[1] += self.gravity
        # check for collision
        self.speed = self.checkCollision(self.rect, wallList, pikaList, self.speed)
        # check for the max speed
        if self.speed[0] >= 70:
            self.speed[0] = 70
        elif self.speed[0] <= -70:
            self.speed[0] = -70

        if self.speed[1] >= 70:
            self.speed[1] = 70
        elif self.speed[1] <= -70:
            self.speed[1] = -70

        self.rect = self.rect.move(self.speed[0], self.speed[1])

        self.rotate += -3 * self.speed[0]
        self.image = rotateCenter(self.imageOrigin, self.rotate)

    def moveOrigin(self, direction):
        pos = self.originPos[direction]
        self.rect = pygame.Rect(pos[0], pos[1], self.width, self.height)
        self.speed = [0, 0]

    def checkPlace(self):
        if self.rect.x > gbv.WINWIDTH or self.rect.x < -self.width:
            if self.rect.y < -self.height or self.rect.y > gbv.WINHEIGHT:
                self.moveOrigin(random.randint(0, 1))

    def update(self, clickButton, wallList, pikaList):
        self.checkMovement(clickButton, wallList, pikaList)
        self.checkPlace()

    def draw(self, DISPLAYSURF):
        DISPLAYSURF.blit(self.image, self.rect)


    def checkCollision(self, tmpRect, wallList, pikaList, ballSpeed):
        wall = tmpRect.collidelist(wallList)
        pika = tmpRect.collidelist(pikaList)
        # check the wall and stick collision
        if wall == -1 and pika == -1:
            return ballSpeed
        else:
            if wall != 4:
                self.ifStickCollision = False

        ballSpeed[0] *= 0.9
        ballSpeed[1] *= 0.9
        if wall == 0:   # left
            if tmpRect.centerx <= 0:
                return [abs(ballSpeed[0])+tmpRect.centerx, ballSpeed[1]]
            else:
                return [abs(ballSpeed[0]), ballSpeed[1]]
        elif wall == 1 or tmpRect.centerx >= gbv.WINWIDTH:   # right
            return [-abs(ballSpeed[0]), ballSpeed[1]]
        elif wall == 2 or tmpRect.centery <= 0:   # up
            return [ballSpeed[0], abs(ballSpeed[1])]
        elif wall == 3 or tmpRect.centery >= gbv.WINHEIGHT:   # down
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
            # check for ball direction
            horizon = (pikaList[pika].rect.centerx-tmpRect.centerx)*0.35
            atSpeed = [speed*pikaList[pika].atLevel for speed in
                       pikaList[pika].atSpeed]
            if horizon < 0:
                return [abs(horizon)+ballSpeed[0]+pikaList[pika].speed[0]*0.05+\
                        atSpeed[0], -35+pikaList[pika].speed[1]*0.3+atSpeed[1]]
            else:
                return [-abs(horizon)+ballSpeed[0]+pikaList[pika].speed[0]*0.05+\
                        atSpeed[0], -35+pikaList[pika].speed[1]*0.3+atSpeed[1]]

        return ballSpeed

def loadImg(path, width, height):
    """
    load the image, and if the reverse == true then flip
    """
    image = pygame.image.load(path).convert()
    image = pygame.transform.scale(image, (width, height))
    transColor = image.get_at((0, 0))
    image.set_colorkey(transColor)
    return image


def rotateCenter(image, angle):
    """rotate an image while keeping its center and size"""
    originRect = image.get_rect()
    rotateImage = pygame.transform.rotate(image, angle)
    rotateRect = originRect.copy()
    rotateRect.center = rotateImage.get_rect().center
    rotateImage = rotateImage.subsurface(rotateRect).copy()
    return rotateImage
