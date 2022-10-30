import pygame, json


class Map_Loader():
    def __init__(self):
        pass

    def Load(self,path):
        with open(path) as file:
            map_data = json.load(file)
        
        return map_data



map_loader = Map_Loader()