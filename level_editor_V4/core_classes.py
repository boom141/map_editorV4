import pygame, os, json
from spritesheet import*

class Game_map():
	def __init__(self):
		pass

	def Labels(self,surface,layer):
		Font = pygame.font.Font(os.path.join('font', 'Minecraft.ttf'), 20)
		coordinates = Font.render(f"X:{pygame.mouse.get_pos()[0]} | Y:{pygame.mouse.get_pos()[1]}",False,'white')
		layer = Font.render(f'Layer: {layer}', False,'white')
		Font1 = pygame.font.Font(os.path.join('font', 'Minecraft.ttf'), 20)
		selection = Font1.render('Image Selection',False,'white')

		surface.blit(selection, (30, 10))
		surface.blit(layer, (260, 10))
		surface.blit(coordinates, (260, 30))
	
	def Initialized_Grid(self,dimensions,tile_size):
		layer = []
		for y in range(0,dimensions[1],tile_size):
			row = []
			for x in range(0,dimensions[0],tile_size):
				row.append([-1])
			layer.append(row)

		return layer

	def Map_Data(self,dimensions,tile_size,layer_count):
		map_data = {}
		for i in range(layer_count):
			map_data[f'DATA {i}'] = self.Initialized_Grid(dimensions,tile_size)
		
		map_data['ENTITY'] = self.Initialized_Grid(dimensions,tile_size)
		return map_data

	def Save_Map(self, map_data):
		with open('save_map/map.json', 'w') as outputfile:
			json.dump(map_data, outputfile)
		print('[MAP SAVE!]')

	def Render_Map(self,map_data,surface,spritesheet):
		for key in map_data:
			for y, list in enumerate(map_data[key]): 
				for x, data in enumerate(list):
					if map_data[key][y][x] != [-1]:
						surface[map_data[key][y][x][0]].blit(spritesheet.image_database[map_data[key][y][x][1]][map_data[key][y][x][2]], 
						(map_data[key][y][x][3],map_data[key][y][x][4]))


game_map = Game_map()