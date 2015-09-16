"""
File: mainScreen.py
Author: Ping
Email: billy3962@hotmail.com
Github: Ping-Lin
Description: show the main game screen and the game process
"""

import pygame
import pygame.freetype
import sys
from pygame.locals import *
import gbv
from character.pika import Pika
from obstacle.wall import Wall
from ball.pikaBall import PikaBall
import button
import socket
import select
import time

class GameClient(object):
    def __init__(self, addr = "127.0.0.1"):
        self.serverPort = 9876
        self.connect = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addr = addr   #server addr
        self.start = False
        self.starting = False

        self.readList = [self.connect]
        self.writeList = []

    def runGame(self, spriteGroup, wallList, pikaList, pikaBall, clickButton, txtImgs,
                buttonGroup):
        """
        Run the main loop of game
        """
        try:
            # Initialize connect to server
            self.connect.sendto('c', (self.addr, self.serverPort))
            clickList = ['0']*12   # receive click list
            sendList = ['0']*5   #send click list
            msg = ""   #send msg
            global NEWGAME, STARTDELAY
            background = pygame.image.load('bg.jpg').convert()
            background = pygame.transform.scale(background, (gbv.WINWIDTH, gbv.WINHEIGHT))
            pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP, MOUSEBUTTONUP])   # improve the FPS
            while True:
                clickList[0:10] = ['0']*10
                sendList[0:] = ['0']*5
                # receive the connect data
                readable, writable, exceptional = (
                    select.select(self.readList, self.writeList, [], 0)
                )
                for f in readable:
                    if f is self.connect:
                        msg, addr = f.recvfrom(32)
                        if len(msg) >= 2:
                            if msg[1] == ',':
                                clickList = [x.strip() for x in msg.split(',')]
                        elif len(msg) == 1:
                            if msg[0] == 'd':
                                print "Good Bye..."
                                exit(1)
                            elif msg[0] == 'c':
                                self.start = True
                            elif msg[0] == 's':
                                if self.start:
                                    self.starting = True
                                else:
                                    self.start = True
                        else:
                            print "Unexpect: {0}".format(msg)
                            exit(1)

                # received data using
                if clickList[0] == '1':
                    clickButton['left'] = True
                if clickList[1] == '1':
                    clickButton['right'] = True
                if clickList[2] == '1':
                    clickButton['up'] = True
                if clickList[3] == '1':
                    clickButton['down'] = True
                if clickList[4] == '1':
                    clickButton['space'] = True
                if clickList[5] == '1':
                    clickButton['a'] = True
                if clickList[6] == '1':
                    clickButton['d'] = True
                if clickList[7] == '1':
                    clickButton['w'] = True
                if clickList[8] == '1':
                    clickButton['s'] = True
                if clickList[9] == '1':
                    clickButton['lshift'] = True

                if clickList[0] == '2':
                    clickButton['left'] = False
                if clickList[1] == '2':
                    clickButton['right'] = False
                if clickList[2] == '2':
                    clickButton['up'] = False
                if clickList[3] == '2':
                    clickButton['down'] = False
                if clickList[4] == '2':
                    clickButton['space'] = False
                if clickList[5] == '2':
                    clickButton['a'] = False
                if clickList[6] == '2':
                    clickButton['d'] = False
                if clickList[7] == '2':
                    clickButton['w'] = False
                if clickList[8] == '2':
                    clickButton['s'] = False
                if clickList[9] == '2':
                    clickButton['lshift'] = False


                for event in pygame.event.get():
                    if event.type == QUIT:
                        self.connect.sendto('d', (self.addr, self.serverPort))
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_F1:
                            pygame.quit()
                            sys.exit()
                        elif event.key == pygame.K_F2:
                            if DISPLAYSURF.get_flags() & FULLSCREEN:
                                pygame.display.set_mode((gbv.WINWIDTH, gbv.WINHEIGHT), DOUBLEBUF, 0)
                            else:
                                pygame.display.set_mode((gbv.WINWIDTH, gbv.WINHEIGHT), FLAGS, 0)
                        elif event.key == pygame.K_a:
                            sendList[0] = '1'
                        elif event.key == pygame.K_d:
                            sendList[1] = '1'
                        elif event.key == pygame.K_w:
                            sendList[2] = '1'
                        elif event.key == pygame.K_s:
                            sendList[3] = '1'
                        elif event.key == pygame.K_LSHIFT:
                            sendList[4] = '1'
                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_a:
                            sendList[0] = '2'
                        elif event.key == pygame.K_d:
                            sendList[1] = '2'
                        elif event.key == pygame.K_w:
                            sendList[2] = '2'
                        elif event.key == pygame.K_s:
                            sendList[3] = '2'
                        elif event.key == pygame.K_LSHIFT:
                            sendList[4] = '2'
                    elif event.type == pygame.MOUSEBUTTONUP:
                        clickPos = pygame.mouse.get_pos()
                        buttonGroup.update(clickPos, pikaList, wallList)

                if not self.start:
                    continue

                msg = ','.join(sendList)
                if msg != '0,0,0,0,0':
                    # set send message
                    self.connect.sendto(msg, (self.addr, self.serverPort))

                # draw the image
                DISPLAYSURF.blit(background, (0, 0))
                pikaBall.drawShadow(DISPLAYSURF)
                spriteGroup.update(clickButton, wallList)

                if STARTDELAY == 0:
                    pos = (float(clickList[10]), float(clickList[11]))
                    pikaBall.update(clickButton, wallList, pikaList, pos)
                else:
                    pikaBall.update(clickButton, wallList, pikaList)

                spriteGroup.draw(DISPLAYSURF)
                buttonGroup.draw(DISPLAYSURF)
                if pikaBall.ifAttack:
                    pikaBall.drawHistory(DISPLAYSURF)
                pikaBall.draw(DISPLAYSURF)
                if pikaBall.ifHitPic:
                    pikaBall.drawHitPic(DISPLAYSURF)

                # check if score
                if wallList[3].ifScore[0] or wallList[3].ifScore[1]:
                    wallList[0].pointSound.play()
                    if not NEWGAME:
                        txtImgs = self.setScore(txtImgs, wallList)
                        NEWGAME = True

                DISPLAYSURF.blit(txtImgs[0], (gbv.MARGINLEFT, gbv.BALLHEIGHT+30))
                DISPLAYSURF.blit(txtImgs[1], (gbv.MARGINRIGHT+30, gbv.BALLHEIGHT+30))

                # check if new game
                if NEWGAME:
                    self.setNewGame(pikaList, pikaBall, wallList)

                pygame.display.update()
                # a new game start need to delay a time

                if STARTDELAY != 0:
                    if STARTDELAY == 1000:
                        pygame.time.delay(STARTDELAY)
                        STARTDELAY = 0
                        self.connect.sendto('s', (self.addr, self.serverPort))
                        if not self.starting:
                            self.start = False
                        self.starting = False
                    else:
                        STARTDELAY = 1000
                        pygame.mixer.music.unpause()

                CLOCK.tick(40)
        finally:
            self.connect.sendto('d', (self.addr, self.serverPort))

    def run(self):
        global IMAGE, DISPLAYSURF, CLOCK, SCORETXT, FONT, ALPHA, NEWGAME, STARTDELAY, FLAGS
        pygame.init()
        pygame.display.set_icon(pygame.image.load('icon.icns'))
        FLAGS = FULLSCREEN | DOUBLEBUF
        DISPLAYSURF = pygame.display.set_mode((gbv.WINWIDTH, gbv.WINHEIGHT), FLAGS, 0)
        DISPLAYSURF.set_alpha(None)
        pygame.display.set_caption('PikaBall X Connect Client')
        CLOCK = pygame.time.Clock()
        FONT = pygame.font.Font(None, 100)
        FONT.set_italic(True)
        pygame.mixer.music.load('bg.wav')

        # Load the element
        pikaLeft = Pika(True)
        pikaRight = Pika()
        pikaList = [pikaLeft, pikaRight]
        spriteGroup = pygame.sprite.Group(pikaLeft)
        spriteGroup.add(pikaRight)
        wallList = []   # left, right, up, down and stick
        wallList.append(
            Wall(pygame.Rect(0, 0, 1, gbv.WINHEIGHT)))
        wallList.append(
            Wall(pygame.Rect(gbv.WINWIDTH, 0, 500, gbv.WINHEIGHT)))
        wallList.append(
            Wall(pygame.Rect(0, 0, gbv.WINWIDTH, 10)))
        wallList.append(
            Wall(pygame.Rect(0, gbv.WINHEIGHT - 50, gbv.WINWIDTH, 500)))
        wallList.append(
            Wall(pygame.Rect(
                gbv.STICKPOS[0], gbv.STICKPOS[1], gbv.STICKWIDTH, gbv.STICKHEIGHT),
                img=True))
        spriteGroup.add(wallList[-1])   # add the stick, need to show
        # spriteGroup.add(wallList)
        musicButton = button.Button(pygame.Rect(gbv.WINWIDTH-200, 20, 60, 60), 1)
        soundButton = button.Button(pygame.Rect(gbv.WINWIDTH-100, 20, 60, 60), 2)
        buttonGroup = pygame.sprite.Group(musicButton)
        buttonGroup.add(soundButton)

        # some initial value
        SCORETXT = [0, 0]
        clickButton = dict.fromkeys(
            ['left', 'right', 'up', 'down', 'space',
            'a', 'd', 'w', 's', 'lshift'])
        txtImgs = [FONT.render("0", 1, (255, 0, 0))]*2
        NEWGAME = False
        ALPHA = 0
        STARTDELAY = 0
        pygame.mixer.music.play(-1, 0.0)
        self.runGame(spriteGroup, wallList, pikaList, PikaBall(),
                clickButton, txtImgs, buttonGroup)


    def setScore(self, txtImgs, wallList):
        if wallList[3].ifScore[0]:
            SCORETXT[0] += 1
        elif wallList[3].ifScore[1]:
            SCORETXT[1] += 1
        txtImgs[0] = FONT.render(str(SCORETXT[0]), 1, (255, 0, 0))
        txtImgs[1] = FONT.render(str(SCORETXT[1]), 1, (255, 0, 0))
        return txtImgs


    def setNewGame(self, pikaList, pikaBall, wallList):
        global NEWGAME, ALPHA, STARTDELAY
        pikaBall.ifAttack = False
        ALPHA += 10
        background = pygame.Surface(DISPLAYSURF.get_size())
        background.set_alpha(ALPHA)
        background.fill((0, 0, 0))
        if ALPHA >= 255:
            NEWGAME = False
            ALPHA = 0
            # set the ball and pika to origin place
            for pika in pikaList:
                pika.moveOrigin()
            if wallList[3].ifScore[0]:
                pikaBall.moveOrigin(0)
            else:
                pikaBall.moveOrigin(1)

            wallList[3].ifScore = [False]*2
            STARTDELAY = 1001
            pygame.mixer.music.pause()

        DISPLAYSURF.blit(background, (0, 0))
        pygame.time.delay(30)

def main(addr='127.0.0.1'):
    player = GameClient(addr)
    player.run()

if __name__ == '__main__':
    main()
