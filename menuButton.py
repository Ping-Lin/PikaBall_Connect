"""
File: button.py
Author: Ping
Email: billy3962@hotmail.com
Github: Ping-Lin
Description: the button for user to click
like 1p vs 1p or connected 1p vs 1p
"""

import pygame
import sys
import mainScreen


class MenuButton(pygame.sprite.Sprite):
    def __init__(self, rect, option):
        super(MenuButton, self).__init__()
        self.rect = rect
        self.option = option
        self.images = []
        self.imageName = 'option' + str(option) + '.bmp'
        self.image = loadImg(self.imageName, rect.w, rect.h)

    def update(self, clickPos, page):
        if self.rect.collidepoint(clickPos):
			if self.option == 1:
				pygame.quit()
				mainScreen.main()
			elif self.option == 2:
				page[0] = 2
			elif self.option == 3 or self.option == 4:
				page[0] = 3


def loadImg(path, width, height):
    """
    load the image
    """
    image = pygame.image.load(path).convert()
    image = pygame.transform.scale(image, (width, height))
    # transColor = image.get_at((0, 0))
    # image.set_colorkey(transColor)
    return image
