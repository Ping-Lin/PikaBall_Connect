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
import server
import client
import re


class MenuButton(pygame.sprite.Sprite):
    def __init__(self, rect, option):
        super(MenuButton, self).__init__()
        self.rect = rect
        self.option = option
        self.images = []
        self.imageName = 'option' + str(option) + '.bmp'
        self.image = loadImg(self.imageName, rect.w, rect.h)

    def update(self, clickPos, page, serverAddr=""):
        """
        option 1: 1p vs 1p
        option 2: connect
        option 3: server
        option 4: client
        option 5: server address correct or not
        """
        if self.rect.collidepoint(clickPos):
            if self.option == 1:
                pygame.quit()
                mainScreen.main()
            elif self.option == 2:
                page[0] = 2
            elif self.option == 3:
                pygame.quit()
                server.main()
            elif self.option == 4:
                page[0] = 3
            elif self.option == 5:
                ifCorrect = checkAddressFormat(serverAddr)
                if ifCorrect:
                    pygame.quit()
                    client.main(serverAddr)
                else:
                    page[0] = -1


def loadImg(path, width, height):
    """
    load the image
    """
    image = pygame.image.load(path).convert()
    image = pygame.transform.scale(image, (width, height))
    # transColor = image.get_at((0, 0))
    # image.set_colorkey(transColor)
    return image


def checkAddressFormat(serverAddr):
    result = re.match(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', serverAddr)
    if result:
        if result.group() == serverAddr:
            return True
    return False
