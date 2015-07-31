"""
File: menu.py
Author: Ping
Email: billy3962@hotmail.com
Github: Ping-Lin
Description: menu let user to select which mode want to play
"""

import pygame
import pygame.freetype
import sys
from pygame.locals import *
import gbv
from menuButton import MenuButton
import eztext

def runGame(buttonGroup, txtImgs, txtbox):
	page = [1]
	while True:
		events = pygame.event.get()
		for event in events:
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONUP:
				clickPos = pygame.mouse.get_pos()
				print clickPos
				if page[0] == 1:
					buttonGroup[0].update(clickPos, page)
				elif page[0] == 2:
					buttonGroup[1].update(clickPos, page)
				elif page[0] == 3:
					pass

		DISPLAYSURF.fill(gbv.BGCOLOR)
		if page[0] == 1:
			buttonGroup[0].draw(DISPLAYSURF)
		elif page[0] == 2:
			buttonGroup[1].draw(DISPLAYSURF)
		elif page[0] == 3:
			txtbox.update(events)
			txtbox.draw(DISPLAYSURF)
		DISPLAYSURF.blit(txtImgs[0], (155, 140))
		pygame.display.update()
		CLOCK.tick(20)


def main():
	global DISPLAYSURF, CLOCK
	pygame.init()
	DISPLAYSURF = pygame.display.set_mode((gbv.WINWIDTH, gbv.WINHEIGHT))
	pygame.display.set_caption('PikaBall X Connect')
	CLOCK = pygame.time.Clock()
	FONT = pygame.font.Font(None, 140)
	
	buttonGroup = []
	buttonGroup.append(pygame.sprite.Group())
	buttonGroup.append(pygame.sprite.Group())
	
	for i in xrange(1, 3):
		button = MenuButton(pygame.Rect(460, 100+200*i, 300, 150), i)
		buttonGroup[0].add(button)
	
	for i in xrange(3, 5):
		button = MenuButton(pygame.Rect(460, 100+200*(i-2), 300, 150), i)
		buttonGroup[1].add(button)
	
	txtImgs = []
	txtImgs.append(FONT.render('PikaBall X Connect', 1, (255, 0, 0)))

	txtbox = eztext.Input(x = 220, y = 417, maxlength = 15, color=(255, 204, 34), prompt='ip: ', font=FONT)

	runGame(buttonGroup, txtImgs, txtbox)
		
if __name__ == '__main__':
	main()
