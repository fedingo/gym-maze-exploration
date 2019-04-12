import pygame
import sys
import time

light_gray = (211, 211, 211)
gray =  (150, 150, 150)
white = (255, 255, 255)
black = (0,   0,   0, )

border_pl = ( 0, 128, 0)
player = (50,205,50)

red_target = (255, 0, 0)
red_border = (76, 0, 19)
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

def draw_target(target_tuple):

	x,y = target_tuple
	pygame.draw.rect(screen, red_border, pygame.Rect(MARGIN + y*SIDE,MARGIN + x*SIDE, SIDE, SIDE))
	pygame.draw.rect(screen, red_target,   pygame.Rect(MARGIN + y*SIDE + BORDER,MARGIN + x*SIDE + BORDER,
														SIDE - 2*BORDER, SIDE - 2*BORDER))
	pygame.display.update()


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