import pygame
from pygame.locals import *
from numpy import loadtxt
import time
import os
from random import randint as randi
#Constants for the game
WIDTH, HEIGHT = (32, 32)
WALL_COLOR = pygame.Color(0, 0, 255, 255) # BLUE
PACMAN_COLOR = pygame.Color(255, 0, 0, 255) # RED
ENEMY_COLOR = pygame.Color(255,255,255)
COIN_COLOR = pygame.Color(255, 255, 0, 255) # RED
DOWN = (0,1)
RIGHT = (1,0)
TOP = (0,-1)
LEFT = (-1,0)
NULL = (0,0) #in case there is a wall we don't want the character to go into the wall
font_name=pygame.font.match_font('comicsans')

#Draws a rectangle for the wall
def draw_wall(screen, pos):
	pixels = pixels_from_points(pos)
	pygame.draw.rect(screen, WALL_COLOR, [pixels, (WIDTH, HEIGHT)])

#Draws a rectangle for the player
def draw_pacman(screen, pos): 
	pixels = pixels_from_points(pos)
	pygame.draw.rect(screen, PACMAN_COLOR, [pixels, (WIDTH, HEIGHT)])

#Draws a rectangle for the enemy
def draw_enemy(screen, pos):
	pixels = pixels_from_points(pos)
	pygame.draw.rect(screen, ENEMY_COLOR, [pixels, (WIDTH, HEIGHT)])

#Draws a rectangle for the coin
def draw_coin(screen, pos):
	pixels = pixels_from_points(pos)
	pygame.draw.rect(screen, COIN_COLOR, [pixels, (WIDTH, HEIGHT)])

#Uitlity functions
def add_to_pos(pos, pos2):
	return (pos[0]+pos2[0], pos[1]+pos2[1])
def pixels_from_points(pos):
	return (pos[0]*WIDTH, pos[1]*HEIGHT)
def scored(surface,text,size,x,y): #this fuction is for showing the score when the player passes any coin tiles
	font = pygame.font.Font(font_name, size)
	text = font.render(text ,True , (255,255,255))
	text_rectangle = text.get_rect()
	text_rectangle.midtop = (x, y)
	screen.blit(text, text_rectangle)
def timed(surface,text,size,x,y):#this function is for timer on the game
	font = pygame.font.Font(font_name, size)
	text = font.render(text ,True , (255,255,255))
	text_rectangle = text.get_rect()
	text_rectangle.midtop = (540, 0)
	screen.blit(text, text_rectangle)

#Initializing pygame
pygame.init()
screen = pygame.display.set_mode((640,640), 0, 32)
background = pygame.surface.Surface((640,640)).convert()
score=0#initialising the score

#Initializing variables
layout = loadtxt('layout.txt', dtype=str)
rows, cols = layout.shape
pacman_position = (1,1)
enemy_position = (18, 18)
background.fill((0,0,0))


# Main game loop
while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()

	screen.blit(background, (0,0))

	#Draw board from the 2d layout array.
  #In the board, '.' denote the empty space, 'w' are the walls, 'c' are the coins
	for col in range(cols):
		for row in range(rows):
			value = layout[row][col]
			pos = (col, row)
			if value == 'w':
				draw_wall(screen, pos)
			elif value == 'c':
				draw_coin(screen, pos)

	#Draw the player
	draw_pacman(screen, pacman_position)
	draw_enemy(screen,enemy_position)#creating the enemy
	
	#TODO: Take input from the user and update pacman moving direction, Currently hardcoded to always move down
	keys = pygame.key.get_pressed()
	if keys[pygame.K_LEFT]:#if left key is pressed
		a1=add_to_pos(pacman_position, LEFT)
		if layout[a1[1],a1[0]]!='w':#checks if there is a wall on the next co-ordinate
			pacman_position = a1
		if layout[a1[1],a1[0]]=='c':#checks if the next location has a coin 
			score +=1
			layout[a1[1], a1[0]] = '.'#replaces coin with a empty tile 
		else:
			continue
	if keys[pygame.K_RIGHT]:
		a2=add_to_pos(pacman_position,RIGHT)
		if layout[a2[1],a2[0]]!= 'w':#check for the wall on the next location
			pacman_position = a2
		if layout[a2[1],a2[0]] == 'c':#checks if the next location has a coin 
			score+=1
			layout[a2[1], a2[0]] = '.'#replaces coin with a empty tile 
		else:
			continue
	if keys[pygame.K_UP]:
		a3=add_to_pos(pacman_position, TOP)
		if layout[a3[1],a3[0]]!= 'w':#check for the wall on the next location
			pacman_position = a3
		if layout[a3[1],a3[0]] == 'c':#checks if the next location has a coin 
			score +=1
			layout[a3[1],a3[0]] = '.'#replaces coin with a empty tile 
		else:
			continue
	if keys[pygame.K_DOWN]:
		a4=add_to_pos(pacman_position,DOWN)
		if layout[a4[1],a4[0]] != 'w':#check for the wall on the next location
			pacman_position = a4
		if layout[a4[1],a4[0]] == 'c':#checks if the next location has a coin 
			layout[a4[1]][a4[0]] = '.'#replaces coin with a empty tile 
			score +=1
		else:
			continue
	#move_direction = DOWN
	#movement of the enemy
	x = randi(0,3)#generating a random integer for the movement of the enemy
	if x == 3 :
		k4 = add_to_pos(enemy_position, DOWN)
		if layout[k4[1], k4[0]] != 'w':
			enemy_position = k4
		else :
			continue
	if x == 2 :
		k3 = add_to_pos(enemy_position, TOP)
		if layout[k3[1], k3[0]] != 'w':
			enemy_position = k3
		else :
			continue
	if x == 1 :
		k2 = add_to_pos(enemy_position, LEFT)
		if layout[k2[1], k2[0]] != 'w':
			enemy_position = k2
		else :
			continue
	if x == 0 :
		k1 = add_to_pos(enemy_position, RIGHT)
		if layout[k1[1], k1[0]] != 'w':
			enemy_position = k1
		else :
			continue
	if pacman_position==enemy_position: #in case enemy and the player collide it should decrease the score by 2 and resets the player location to 1,1 which was the starting position
		pacman_position = [1,1]
		score -=2
	if pacman_position == (18, 9):
		pacman_position = (1, 9)
	if pacman_position == (1, 9):
		pacman_position = (18, 9)
	print(pacman_position)
	#Update player position based on movement.
	#pacman_position = add_to_pos(pacman_position, move_direction)

	#TODO: Check if player ate any coin, or collided with the wall by using the layout array.
	# player should stop when colliding with a wall
	# coin should dissapear when eating, i.e update the layout array
	scored(screen, "Score : " + str(score), 20, 75, 1) #this is for updating the score each time the loop runs (updatation depends upon the score)
	#Update the display
	timed(screen, "Time : " + str(int(pygame.time.get_ticks()/1000)), 20, 75, 1)#this is for the timer on the top to show how much time has elapsed

	pygame.display.update()
	#Wait for a while, computers are very fast.
	time.sleep(0.5)
