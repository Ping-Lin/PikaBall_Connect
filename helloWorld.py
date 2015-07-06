import pygame, sys
from pygame.locals import *

BLUE = (0, 0, 255)

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 300), 0, 32)
pygame.display.set_caption('hello world!')
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.quit()
        pygame.draw.circle(DISPLAYSURF, BLUE, (300, 50), 20, 0)
    pygame.display.update()
