"""
File: pika.py
Author: Ping
Email: billy3962@hotmail.com
Github: Ping-Lin
Description: pika.py store the information of the pika character
"""
import pygame
import gbv


class Pika(pygame.sprite.Sprite):
    def __init__(self):
        super(Pika, self).__init__()

        # Load the pika image
        self.pikaImages = []
        for i in xrange(1, 6):
            path = 'character/pikaToRight' + str(i) + '.bmp'
            self.pikaImages.append(loadImage(path))

        # initialize the image and rect
        self.index = 0
        self.image = self.pikaImages[self.index]
        self.rect = pygame.Rect(gbv.MARGINRIGHT, gbv.MARGINHEIGHT, 256, 256)

    def update(self):
        self.index += 1
        if self.index >= len(self.pikaImages):
            self.index = 0
        self.image = self.pikaImages[self.index]


def loadImage(path):
    image = pygame.image.load(path).convert()
    transColor = image.get_at((0, 0))
    image.set_colorkey(transColor)
    return image
