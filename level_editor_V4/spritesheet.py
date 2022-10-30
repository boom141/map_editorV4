from tkinter import Button
import pygame, os

class Spritesheet():
	def __init__(self,root_folder):
		self.root_folder = root_folder
		self.image_database = {}
		self.buttons_color = 'white'
		self.current_folder = [-1,-1]
		self.sprite_data = None

		for folder in os.listdir(root_folder):
			image_con = []
			for file in os.listdir(f'{root_folder}/{folder}'):
				image = pygame.image.load(f'{root_folder}/{folder}/{file}').convert()
				image.set_colorkey((0,0,0))
				image_con.append(image)
			self.image_database[f'{folder}'] = image_con

	def Folder_Selection(self,surface):
		buttons = []
		for i, folder in enumerate(os.listdir(self.root_folder)):
			if self.current_folder[1] == i:
				self.buttons_color = 'grey'
			else:
				self.buttons_color = 'white' 

			Font = pygame.font.Font(os.path.join('font', 'Minecraft.ttf'), 15)
			folder_name = Font.render(folder, False, self.buttons_color)
			buttons.append([folder,surface.blit(folder_name,(30,(i+2)*20))])
		
		pygame.draw.line(surface, 'white', (0,190), (250,190))
		
		for button in buttons: 
			if pygame.mouse.get_pressed()[0] and button[1].collidepoint(pygame.mouse.get_pos()):
				self.current_folder = [button[0],buttons.index(button)]
				self.sprite_data = None
	
	def Tile_Selection(self,surface):
		if -1 not in self.current_folder:
			buttons = []
			selection = self.image_database[self.current_folder[0]]
			for i, image in enumerate(selection):
				image_scaled = pygame.transform.scale(image,(30,30))
				buttons.append(surface.blit(image_scaled,(30,(i+6)*35)))
			
			for button in buttons:
				if pygame.mouse.get_pressed()[0] and button.collidepoint(pygame.mouse.get_pos()):
					self.sprite_data = [self.current_folder[0],buttons.index(button)]

			if self.sprite_data != None:
				pygame.draw.rect(surface, 'green', (buttons[self.sprite_data[1]].x - 5,buttons[self.sprite_data[1]].y - 5,40,40), 1)