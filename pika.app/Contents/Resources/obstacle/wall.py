"""
File: wall.py
Author: Ping
Email: billy3962@hotmail.com
Github: Ping-Lin
Description: this class is for the collision of the sprites, including the
boundaries and the stick
"""

import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, rect, img=False):
        super(Wall, self).__init__()
        self.rect = rect
        self.ifScore = [False]*2
        # if there is image upload it
        if img:
            path = 'obstacle/stick.bmp'
            self.image = pygame.image.load(path).convert()
            self.image = pygame.transform.scale(self.image, (rect.w, rect.h))

        # sound
        self.pointSound = pygame.mixer.Sound('obstacle/point.wav')
        self.pointSound.set_volume(0.5)
        # color for test
        # self.image = pygame.Surface([self.rect.w, self.rect.h])
        # self.image.fill((0, 0, 255))
