import pygame
import noise
import random


#map size
tile_s = 8
map_w = 200
map_h = 150
screen_w = 800
screen_h = 600
max_x_tiles = screen_w - tile_s
max_y_tiles = screen_h - tile_s

#perlin settings
scale = 80 #zoom
octaves = 6 #detail
persistence = 0.55 #roughness
lacunarity = 2.1 #scale increase per octave

#fog matrix and stuff
fog = [[False for _ in range(map_w)]for _ in range(map_h)]
fog_d = False

#minimap stuf
mini_e = True
mini_s = 200
mini_i = pygame.Surface(map_w, map_h)

#set up
pygame.init()
screen = (screen_w, screen_h)
pygame.display.set_caption("Procedural Landmass Generation")
clock = pygame.time.Clock()

#seed stuff for perlin sound
seed = random.randint(0, 500) #dont put it too high or maps look goofy and crash
print("Your seed is:", seed)

#terain gen
def terain_data(x, y):
    a = x / scale
    b = y / scale

    c = noise.pnoise2(a, b, octaves = octaves, persistence = persistence, lacunarity = lacunarity, rx = map_w, ry = map_h, bs = seed) #makes values from -1.0 - 1.0

    colour = (c + 1)/2

    if colour < 0.3:
        return (0, 0, 128) #deep water
    elif colour < 0.4:
        return (0, 0, 255) #shallow water
    elif colour < 0.45:
        return (194, 178, 128) #sand
    elif colour < 0.6:
        return (34, 139, 34) #grass
    elif colour < 0.7:
        return (211, 211, 211) #rocks
    else:
        return (255, 255, 255) #mountain
    
#map gen
def map_gen():
    global tile_m
    global fog

    tile_m = []
    fog = [[False for _ in range(map_w)]for _ in range(map_h)]

    for y in range (map_h):
        row = []
        for x in range(map_w):
            color, passable = terain_data(x, y)
            row.append({'color': color, 'passable': passable})
        tile_m.append(row)

#build map
map_gen()

#player
player_pos = [map_w // 2, map_h // 2]
player_colour = (255, 0, 0)
player_radius = tile_s
