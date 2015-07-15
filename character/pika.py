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

        # pika width and height amd position
        self.width = 180
        self.height = 180
        if not reverse:
            self.originPos = (gbv.MARGINRIGHT, gbv.MARGINHEIGHT)
        else:
            self.originPos = (gbv.MARGINLEFT, gbv.MARGINHEIGHT)

        # Load the pika image: walk, pu, jump
        self.pikaImgs = []
        for i in xrange(1, 6):
            path = 'character/pikaToRight' + str(i) + '.bmp'
            self.pikaImgs.append(
                loadImg(path, reverse, self.width, self.height))

        self.puImgs = [None]*10
        for i in xrange(1, 11):
            j = i-5 if i > 5 else i
            j = 3 if j >= 4 else j
            path = 'character/pikaPu' + str(j) + '.bmp'
            if i <= 5:
                self.puImgs[i-1] = loadImg(path, False, self.width, self.height)
            else:
                self.puImgs[i-1] = loadImg(path, True, self.width, self.height)

        self.atImgs = [None]*12
        for i in xrange(1, 13):
            j = i-6 if i > 6 else i
            path = 'character/pikaAt' + str(j) + '.bmp'
            if i <= 6:
                self.atImgs[i-1] = loadImg(path, False, self.width, self.height)
            else:
                self.atImgs[i-1] = loadImg(path, True, self.width, self.height)

        # sound, pu, attack
        self.sound = [None]*2
        self.sound[0] = pygame.mixer.Sound('character/pu.wav')
        self.sound[1] = pygame.mixer.Sound('character/attack.wav')
        for sound in self.sound:
            sound.set_volume(0.5)

        # direction and motion
        self.direct = reverse
        self.jump = False
        self.jumpingNow = False
        self.pu = False
        self.puingNow = False
        self.attack = False
        self.attackingNow = False
        self.atLevel = 0
        self.atLevelId = 0

        # now speed, gravity, jump height, attack Speed, constant walk Speed,
        # current attack, speed, constant attack speed,
        self.speed = [0, 0]
        self.gravity = gbv.GRAVITY
        self.pikaHeight = 300
        self.pikaV0 = -50
        self.constWalkSpeed = 18
        self.atSpeed = [0, 0]
        self.constAtSpeed = [15, 2, 30]   #left(right), up and down

        # initialize the image and rect
        self.index = 0
        self.indexPu = 0
        self.indexAt = 0
        self.image = self.pikaImgs[self.index]
        if not reverse:
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
                self.speed[0] -= self.constWalkSpeed
                self.atSpeed[0] = -self.constAtSpeed[0]
            if clickButton['right']:
                self.speed[0] += self.constWalkSpeed
                self.atSpeed[0] = self.constAtSpeed[0]
            if clickButton['up']:
                self.jump = True
                self.atSpeed[1] = -self.constAtSpeed[1]
            if clickButton['down']:
                self.atSpeed[1] = self.constAtSpeed[2]
            if clickButton['space']:
                self.attack = self.pu = True
        else:
            if clickButton['a']:
                self.speed[0] -= self.constWalkSpeed
                self.atSpeed[0] = -self.constAtSpeed[0]
            if clickButton['d']:
                self.speed[0] += self.constWalkSpeed
                self.atSpeed[0] = self.constAtSpeed[0]
            if clickButton['w']:
                self.jump = True
                self.atSpeed[1] = -self.constAtSpeed[1]
            if clickButton['s']:
                self.atSpeed[1] = self.constAtSpeed[2]
            if clickButton['lshift']:
                self.attack = self.pu = True

        # jumping or not
        if self.jump and not self.jumpingNow and not self.puingNow:
            self.speed[1] = self.pikaV0
            self.jumpingNow = True
        if self.jumpingNow:
            self.speed[1] += self.gravity
            if self.attack:   # jumping then can attack
                self.attackingNow = True
                self.sound[1].play()
                self.indexAt = 0
                self.atLevel += 1
        if self.rect.y + self.speed[1] >= gbv.MARGINHEIGHT:
            self.speed[1] = gbv.MARGINHEIGHT - self.rect.y
            self.jumpingNow = False

        # puing or not
        if self.pu and not self.puingNow and not self.jumpingNow and \
                not self.attackingNow:
            self.indexPu = 0
            self.puingNow = True
            self.sound[0].play()
        if self.puingNow:
            self.indexPu += 1
            index = self.indexPu / 3
            if index == 4:
                self.puingNow = False
            if self.direct and not clickButton["a"] or clickButton["right"]:
                self.image = self.puImgs[index]
                self.speed[0] = 14 if index % 5 <= 2 else 0
            else:
                self.image = self.puImgs[index + 5]
                self.speed[0] = -14 if index % 5 <= 2 else 0

        # attacking or not
        if self.attackingNow:
            self.indexAt += 1
            index = self.indexAt / 3
            if index == 5:
                self.attackingNow = False
                self.atLevel = 0
                self.atSpeed = [0, 0]
            if index == 0:
                self.atLevelId += 1
                if self.atLevelId >= 10:
                    self.atLevelId = 0
                if self.atLevelId >= 5:
                    newIndex = 1
                else:
                    newIndex = 0
            else:
                self.sound[1].play()
                newIndex = index
            if self.direct:
                self.image = self.atImgs[newIndex]
            else:
                self.image = self.atImgs[newIndex + 6]

        # check for collision
        tmpRect = self.rect.move(self.speed[0], self.speed[1])
        if checkCollision(tmpRect, wallList):
            self.rect = self.rect.move(0, self.speed[1])
        else:
            self.rect = tmpRect

    def moveOrigin(self):
        self.rect = pygame.Rect(self.originPos[0], self.originPos[1],
                                self.width, self.height)

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
        if index >= len(self.pikaImgs):
            self.index = 0
            index = 0
        self.image = self.pikaImgs[index]
        # check movement
        self.checkMovement(clickButton, wallList)


def loadImg(path, reverse, width, height):
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
