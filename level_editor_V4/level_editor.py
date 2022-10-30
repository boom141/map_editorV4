import pygame, time, sys, os
from core_classes import*
from spritesheet import*
from map_loader import*
from pygame.locals import *

pygame.init()


WINDOW_DIMENSION = (800,600)
LAYER_DIMENSION = (2000,2000)
SPEED = 5
LAYER_COUNT = 5
TILE_SIZE = 16

window = pygame.display.set_mode(WINDOW_DIMENSION)
layers = []
for i in range(LAYER_COUNT):
	layers.append(pygame.Surface(LAYER_DIMENSION, pygame.SRCALPHA))
spritesheet_section = pygame.Surface((250,600))
fps = pygame.time.Clock()
last_time = time.time()
scroll = [-800,-600]

up,down,left,right = False,False,False,False
change_layer = False

current_layer = LAYER_COUNT
clicked_once = 0

spritesheet = Spritesheet('images')

map_data = {}
while True:
	print('1: NEW MAP\n2: LOAD MAP')
	number = int(input('ENTER CHOICE: '))
	if number == 1:
		map_data = game_map.Map_Data(LAYER_DIMENSION,TILE_SIZE,LAYER_COUNT)
		break
	elif number == 2:
		file_name = input('ENTER FILE NAME: ')
		map_data = map_loader.Load(f'save_map/{file_name}')
		print('[LOAD SUCCESSFULLY!]')
		break

while True:
# surface fill -----------------------------------------------------------#
	window.fill((0,0,0))
	for index, layer in enumerate(layers):
		layer.fill((0,0,0))
		layer.set_colorkey((0,0,0))
	spritesheet_section.fill((25,25,25))

# framerate independence -------------------------------------------------#
	dt = time.time() - last_time
	dt *= 60
	last_time = time.time()

# coordinates ------------------------------------------------------------#
	mouse = pygame.mouse.get_pos()
	gridx = int((mouse[0] - scroll[0])/TILE_SIZE)
	gridy = int((mouse[1] - scroll[1])/TILE_SIZE)

# move surface -----------------------------------------------------------#
	move = [0,0]
	if up:
		move[1] -= SPEED * dt
	if down:
		move[1] += SPEED * dt
	if left:
		move[0] -= SPEED * dt
	if right:
		move[0] += SPEED * dt

	scroll[0] +=  move[0]
	scroll[1] +=  move[1]

# features ---------------------------------------------------------------#
	spritesheet.Folder_Selection(spritesheet_section)
	spritesheet.Tile_Selection(spritesheet_section)
	
	if change_layer and clicked_once == 0:
		current_layer -= 1
		if current_layer <= 0:
			current_layer = LAYER_COUNT
		clicked_once = 1
	

	if mouse[0] > spritesheet_section.get_width() and pygame.MOUSEMOTION:
		# hovering feature ----------------------------------------------#
		if spritesheet.sprite_data != None:
			image = spritesheet.image_database[spritesheet.sprite_data[0]][spritesheet.sprite_data[1]]
			window.blit(image,(mouse[0] - image.get_width()//2,mouse[1] - image.get_height()//2))
		# draw on to surface --------------------------------------------#
		if pygame.mouse.get_pressed()[0]:
			if map_data[f'DATA {current_layer - 1}'][gridy][gridx] != spritesheet.sprite_data:
				if spritesheet.current_folder[0] == 'decoration' or spritesheet.current_folder[0] == 'foliage':
					image = spritesheet.image_database[spritesheet.sprite_data[0]][spritesheet.sprite_data[1]]
					map_data[f'DATA {current_layer - 1}'][gridy][gridx] = [(current_layer - 1),spritesheet.sprite_data[0],spritesheet.sprite_data[1],(mouse[0] - image.get_width()//2) - scroll[0],(mouse[1] - image.get_height()//2) - scroll[1]]
				elif spritesheet.current_folder[0] == 'entity':
					map_data['ENTITY'][gridy][gridx] = [(current_layer - 1),spritesheet.sprite_data[0],spritesheet.sprite_data[1],gridx*TILE_SIZE,gridy*TILE_SIZE]
				else:
					map_data[f'DATA {current_layer - 1}'][gridy][gridx] = [(current_layer - 1),spritesheet.sprite_data[0],spritesheet.sprite_data[1],gridx*TILE_SIZE,gridy*TILE_SIZE]
		# erase image from the surface ----------------------------------#	
		if pygame.mouse.get_pressed()[2]:
			if map_data[f'DATA {current_layer - 1}'][gridy][gridx] != [-1]:
				map_data[f'DATA {current_layer - 1}'][gridy][gridx] = [-1]

	game_map.Render_Map(map_data,layers,spritesheet)
	
	if pygame.key.get_pressed()[K_SPACE]:
		game_map.Save_Map(map_data)

# event handler ----------------------------------------------------------#   

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
			if event.key == pygame.K_w:    
				up = True
			if event.key == pygame.K_s:
				down = True
			if event.key == pygame.K_a:
				left = True
			if event.key == pygame.K_d:
				right = True
			if event.key == pygame.K_DOWN:
				change_layer = True

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_w:    
				up = False
			if event.key == pygame.K_s:
				down = False
			if event.key == pygame.K_a:
				left = False
			if event.key == pygame.K_d:
				right = False
			if event.key == pygame.K_DOWN:
				change_layer = False
				clicked_once = 0

	for layer in layers:
		pygame.draw.rect(layer, 'red', (0,0,LAYER_DIMENSION[0],LAYER_DIMENSION[1]),2)
		window.blit(layer, (scroll[0],scroll[1]))
		window.blit(spritesheet_section, (0,0))

	game_map.Labels(window,current_layer)

	pygame.display.update()
	fps.tick(60)


