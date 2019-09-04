import pygame
import sys
import time
import numpy as np

light_gray = (211, 211, 211)
gray =  (150, 150, 150)
white = (255, 255, 255)
black = (0,   0,   0, )

border_pl = ( 0, 128, 0)
player = (50,205,50)

color_dict = {
	"red"   : [(255,   0,   0), ( 76,   0, 19)],
	"green" : [(0  , 255,   0), (  0, 178, 0)],
	"blue"  : [(0  ,   0, 255), (  0,   0, 178)],
	"yellow": [(255, 255,   0), (178, 178, 0)]
}

block_color =  (160, 160, 160)
border_color = (100, 100, 100)

screen = None
SIDE = 50
BORDER = 3
MARGIN = 5
LINE = 2

def __draw_ground(x,y):
	pygame.draw.rect(screen, border_color, pygame.Rect(MARGIN + y*SIDE,MARGIN + x*SIDE, SIDE, SIDE))
	pygame.draw.rect(screen, light_gray,   pygame.Rect(MARGIN + y*SIDE + LINE,MARGIN + x*SIDE + LINE,
														SIDE - 2*LINE, SIDE - 2*LINE))

def __draw_wall(x,y):

	pygame.draw.rect(screen, border_color, pygame.Rect(MARGIN + y*SIDE,MARGIN + x*SIDE, SIDE, SIDE))
	pygame.draw.rect(screen, block_color,  pygame.Rect(MARGIN + y*SIDE + BORDER, MARGIN + x*SIDE + BORDER,
													   SIDE - 2*BORDER, SIDE - 2*BORDER))


def draw_player(player_tuple):

	x,y = player_tuple
	pygame.draw.circle(screen, border_pl, (MARGIN + y*SIDE + SIDE//2,MARGIN + x*SIDE + SIDE//2), SIDE//2)
	pygame.draw.circle(screen, player, (MARGIN + y*SIDE + SIDE//2,MARGIN + x*SIDE + SIDE//2), SIDE//2 - BORDER)
	pygame.display.update()


def draw_player_with_dir(player_tuple, dir):

	x, y = player_tuple
	dir += 2
	point_list = [(0, 0), (SIDE, 0), (SIDE // 2, SIDE)]

	ent = pygame.Surface([SIDE, SIDE], pygame.SRCALPHA, 32)
	pygame.draw.polygon(ent, player, point_list)
	screen.blit(pygame.transform.rotate(ent, 90 * dir), pygame.Rect(MARGIN + y * SIDE, MARGIN + x * SIDE, SIDE, SIDE))
	pygame.display.update()


def draw_target(tuple, color = "red"):

	target, border =  color_dict[color]
	x_array, y_array = tuple

	if isinstance(x_array, list) or isinstance(y_array, np.ndarray):
		if len(x_array) == 0:
			return
	else:
		x_array = [x_array]
		y_array = [y_array]

	for x,y in zip(x_array, y_array):

		pygame.draw.rect(screen, border, pygame.Rect(MARGIN + y*SIDE,MARGIN + x*SIDE, SIDE, SIDE))
		pygame.draw.rect(screen, target,   pygame.Rect(MARGIN + y*SIDE + BORDER,MARGIN + x*SIDE + BORDER,
															SIDE - 2*BORDER, SIDE - 2*BORDER))
	pygame.display.update()


def reset_screen():
	global screen
	screen = None

## Render function for the unblockme_class
def render(matrix):

	k, h = matrix.shape

	global screen 
	if screen is None:
		pygame.init()
		screen = pygame.display.set_mode((2*MARGIN+h*SIDE, 2*MARGIN+k*SIDE))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.display.quit()
			pygame.quit()
			sys.exit(0)

	screen.fill(light_gray)

	# first we draw the background
	for x in range(0,k):
		for y in range(0,h):
			# Draw the background with the grid pattern
			__draw_ground(x,y)
	
	# then we draw the blocks in the grid
	for x in range(0,k):
		for y in range(0,h):
			if matrix[x,y] == 1:
			   __draw_wall(x,y)

	pygame.display.update()


def get_action():

	action = -1
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.display.quit()
			pygame.quit()
			sys.exit(0)
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				action = 3
			elif event.key == pygame.K_RIGHT:
				action = 2
			elif event.key == pygame.K_UP:
				action = 0
			elif event.key == pygame.K_DOWN:
				action = 1

	return action