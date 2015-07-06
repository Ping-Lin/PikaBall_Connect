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
    def __init__(self, reverse=False):
        super(Pika, self).__init__()

        # Load the pika image
        self.pikaImages = []
        for i in xrange(1, 6):
            path = 'character/pikaToRight' + str(i) + '.bmp'
            self.pikaImages.append(loadImage(path, reverse))

        # initialize the image and rect
        self.index = 0
        self.image = self.pikaImages[self.index]
        if reverse == False:
            self.rect = pygame.Rect(gbv.MARGINRIGHT, gbv.MARGINHEIGHT, 64, 64)
        else:
            self.rect = pygame.Rect(gbv.MARGINLEFT, gbv.MARGINHEIGHT, 64, 64)

    def update(self):
        self.index += 1
        if self.index >= len(self.pikaImages):
            self.index = 0
        self.image = self.pikaImages[self.index]


def loadImage(path, reverse):
    image = pygame.image.load(path).convert()
    image = pygame.transform.flip(image, reverse, False)
    image = pygame.transform.scale(image, (128, 128))
    transColor = image.get_at((0, 0))
    image.set_colorkey(transColor)
    return image
