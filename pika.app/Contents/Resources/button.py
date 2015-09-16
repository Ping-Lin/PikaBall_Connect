"""
File: button.py
Author: Ping
Email: billy3962@hotmail.com
Github: Ping-Lin
Description: the button for user to click
like stop the music or the sound
"""

import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, rect, option):
        super(Button, self).__init__()
        self.rect = rect
        self.ifOpen = True
        self.option = option
        self.images = []

        if option == 1:   # stop the sound
            self.images.append(loadImg("musicOn.png", rect.w, rect.h))
            self.images.append(loadImg("musicOff.png", rect.w, rect.h))
        elif option == 2:   # stop the music
            self.images.append(loadImg("soundOn.png", rect.w, rect.h))
            self.images.append(loadImg("soundOff.png", rect.w, rect.h))

        # initial the image
        self.image = self.images[0]

    def update(self, clickPos, pikaList, wallList):
        if self.rect.collidepoint(clickPos):
            if self.option == 1:
                if self.ifOpen:
                    pygame.mixer.music.stop()
                    self.ifOpen = False
                    self.image = self.images[1]
                else:
                    pygame.mixer.music.play()
                    self.ifOpen = True
                    self.image = self.images[0]
            elif self.option == 2:
                for pika in pikaList:
                    for sound in pika.sound:
                        if self.ifOpen:
                            sound.set_volume(0)
                        else:
                            sound.set_volume(0.5)
                if self.ifOpen:
                    self.ifOpen = False
                    self.image = self.images[1]
                    wallList[0].pointSound.set_volume(0)
                else:
                    self.ifOpen = True
                    self.image = self.images[0]
                    wallList[0].pointSound.set_volume(0.5)


def loadImg(path, width, height):
    """
    load the image
    """
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, (width, height))
    return image
