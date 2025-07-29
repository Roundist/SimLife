import pygame
import noise
import random

tile_s = 10
map_w, map_h = 200, 150
screen_w, screen_h = 800, 600

v_tiles_x = screen_w // tile_s
v_tiles_y = screen_h // tile_s


pygame.init()
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("Fog of War + Biomes + Minimap")
clock = pygame.time.Clock()

seed = random.randint(0, 250)
print("Your seed is:", seed)

scale = 80.0

fog = [[False for _ in range(map_w)] for _ in range(map_h)]
fog_disabled = False


show_minimap = True
minimap_size = 200
minimap_surface = pygame.Surface((map_w, map_h))


def get_tile_data(x, y):
    nx = x / scale
    ny = y / scale
    raw = noise.pnoise2(nx, ny, octaves=6, persistence=0.55, lacunarity=2.1, base=seed)
    val = (raw + 1) / 2

    if val < 0.3:
        return (0, 0, 128), False
    elif val < 0.4:
        return (0, 0, 255), False
    elif val < 0.45:
        return (194, 178, 128), True
    elif val < 0.6:
        return (34, 139, 34), True
    elif val < 0.72:
        return (0, 100, 0), True
    else:
        return (139, 137, 137), False

def generate_map():
    global tile_map, fog
    tile_map = []
    fog = [[False for _ in range(map_w)] for _ in range(map_h)]
    for y in range(map_h):
        row = []
        for x in range(map_w):
            color, passable = get_tile_data(x, y)
            row.append({'color': color, 'passable': passable})
        tile_map.append(row)

generate_map()


player_pos = [map_w // 2, map_h // 2]
player_color = (255, 0, 0)
player_radius = tile_s

def draw_minimap():
    minimap_surface.fill((0, 0, 0))
    for y in range(map_h):
        for x in range(map_w):
            if fog[y][x]:
                color = tile_map[y][x]['color']
                minimap_surface.set_at((x, y), color)
    scaled = pygame.transform.scale(minimap_surface, (minimap_size, minimap_size * map_h // map_w))
    screen.blit(scaled, (screen_w - minimap_size - 10, 10))

    px = int(player_pos[0] * minimap_size / map_w)
    py = int(player_pos[1] * minimap_size / map_w)
    pygame.draw.circle(screen, player_color, (screen_w - minimap_size - 10 + px, 10 + py), 3)

def update_fog():
    vision_radius = 10
    px, py = player_pos
    for dy in range(-vision_radius, vision_radius + 1):
        for dx in range(-vision_radius, vision_radius + 1):
            tx = px + dx
            ty = py + dy
            if 0 <= tx < map_w and 0 <= ty < map_h:
                fog[ty][tx] = True

running = True
while running:
    dt = clock.tick(60)
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                show_minimap = not show_minimap
            elif event.key == pygame.K_r:
                seed = random.randint(0, 250)
                print("New Seed:", seed)
                generate_map()
                fog_disabled = False
            elif event.key == pygame.K_f:
                fog_disabled = True
                for y in range(map_h):
                    for x in range(map_w):
                        fog[y][x] = True

    keys = pygame.key.get_pressed()
    dx = dy = 0
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        dy = -1
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        dy = 1
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        dx = -1
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        dx = 1

    new_x = player_pos[0] + dx
    new_y = player_pos[1] + dy
    if 0 <= new_x < map_w and 0 <= new_y < map_h:
        if tile_map[new_y][new_x]['passable']:
            player_pos = [new_x, new_y]

    if not fog_disabled:
        update_fog()

    top_left_x = player_pos[0] - v_tiles_x // 2
    top_left_y = player_pos[1] - v_tiles_y // 2

    for y in range(v_tiles_y):
        for x in range(v_tiles_x):
            map_x = top_left_x + x
            map_y = top_left_y + y
            if 0 <= map_x < map_w and 0 <= map_y < map_h:
                if fog[map_y][map_x]:
                    color = tile_map[map_y][map_x]['color']
                else:
                    color = (20, 20, 20)
                pygame.draw.rect(screen, color, (x * tile_s, y * tile_s, tile_s, tile_s))

    pygame.draw.circle(screen, player_color, (screen_w // 2, screen_h // 2), player_radius)

    if show_minimap:
        draw_minimap()

    pygame.display.flip()

pygame.quit()
