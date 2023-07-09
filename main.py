import pygame
import random
import os

WIDTH = 512  # ширина игрового окна
HEIGHT = 512 # высота игрового окна
FPS = 16 # частота кадров в секунду
DIM = 32
TILE_SIZE = 16

pygame.init()
# pygame.mixer.init()  # для звука
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WFC")
clock = pygame.time.Clock()

from tile import Tile, TileSprite

grid = []
for i in range(DIM ** 2):
    grid.append(Tile())
# print(grid)
# grid[2].collapsed = True
# grid[3].collapsed = True
# grid[2].options = [1, 2]
# grid[3].options = [3, 4]

EMPTY = 0
HORIZONTAL = 1
T_LEFT = 2
T_RIGHT = 3
CROSS = 4
rules = [
    [ # EMPTY
        [EMPTY, HORIZONTAL], # up
        [EMPTY, T_RIGHT], # right
        [EMPTY, HORIZONTAL], # down
        [EMPTY, T_LEFT], # left
    ],
    [ # HORIZONTAL
        [EMPTY, HORIZONTAL], # up
        [HORIZONTAL, T_LEFT, CROSS], # right
        [EMPTY, HORIZONTAL], # down
        [HORIZONTAL, T_RIGHT, CROSS], # left
    ],
    [ # T_LEFT
        [T_LEFT, T_RIGHT, CROSS], # up
        [EMPTY, T_RIGHT], # right
        [T_LEFT, T_RIGHT, CROSS], # down
        [HORIZONTAL, T_RIGHT, CROSS], # left
    ],
    [ # T_RIGHT
        [T_LEFT, T_RIGHT, CROSS], # up
        [HORIZONTAL, T_LEFT, CROSS], # right
        [T_LEFT, T_RIGHT, CROSS], # down
        [EMPTY, T_LEFT], # left
    ],
    [ # CROSS
        [T_LEFT, T_RIGHT, CROSS], # up
        [HORIZONTAL, T_LEFT, CROSS], # right
        [T_LEFT, T_RIGHT, CROSS], # down
        [HORIZONTAL, T_RIGHT, CROSS], # left
    ],
]

all_sprites = pygame.sprite.Group() 

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'tiles')

tile_mapping = {
    0: 'empty.png',
    1: 'horizontal.png',
    2: 't_left.png',
    3: 't_right.png',
    4: 'cross.png',
}

def checkValid(options, valid):
    return list(filter(lambda option: option in valid, options))

running = True
while running:
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Обновление
    all_sprites.update()
    
    # Рендеринг
    screen.fill(0)
    # for i, sprite in enumerate(all_sprites):
    #     sprite.rect.x = i * 16
    # all_sprites.draw(screen)

    by_entropy = sorted(filter(lambda tile: not tile.collapsed, grid), key=lambda tile: len(tile.options))
    # print(f'by_entropy preview {sorted(list(map(lambda tile: len(tile.options) + 1000 * int(tile.collapsed), grid)))}')
    # print(f'{by_entropy=}')
    to_collapse = list(filter(lambda tile: len(tile.options) == len(by_entropy[0].options), by_entropy))
    print(to_collapse)
    if to_collapse:
        to_collapse = random.choice(to_collapse)
        try:
            to_collapse.collapse()
        except IndexError:
            print('Fuck!')
            running = False
            break

    for j in range(DIM):
        for i in range(DIM):
            cell = grid[i + j * DIM]
            if (cell.collapsed):
                sprite = TileSprite(tile_mapping[cell.options[0]])
                sprite.rect.x = i * TILE_SIZE
                sprite.rect.y = j * TILE_SIZE
                all_sprites.add(sprite)
    all_sprites.draw(screen)

    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

    for i in range(DIM):
        nextTiles = []
        for j in range(DIM):
            for i in range(DIM):
                cell = grid[i + j * DIM]
                if (cell.collapsed):
                    nextTiles.append(cell)
                else:
                    options = cell.options.copy()
                    # print(f'start options {i} {j}: {options}')
                    # UP
                    if (j > 0):
                        up = grid[i + (j - 1) * DIM]
                        validOptions = set()
                        for option in up.options:
                            valid = rules[option][2]
                            validOptions.update(valid)
                        options = checkValid(options, validOptions)
                    # print(f'up options {i} {j}: {options}')
                    # RIGHT
                    if (i < DIM - 1):
                        right = grid[(i + 1) + j * DIM]
                        validOptions = set()
                        for option in right.options:
                            valid = rules[option][3]
                            validOptions.update(valid)
                        options = checkValid(options, validOptions)
                    # print(f'right options {i} {j}: {options}')
                    # DOWN
                    if (j < DIM - 1):
                        down = grid[i + (j + 1) * DIM]
                        validOptions = set() ## 00 11 10 01
                        for option in down.options:
                            valid = rules[option][0]
                            validOptions.update(valid)
                        options = checkValid(options, validOptions)
                    # print(f'down options {i} {j}: {options}')
                    # LEFT
                    if (i > 0):
                        left = grid[(i - 1) + j * DIM]
                        validOptions = set()
                        for option in left.options:
                            valid = rules[option][1]
                            validOptions.update(valid)
                        options = checkValid(options, validOptions)
                            
                    # print(f'left options {i} {j}: {options}')
                    nextCell = Tile()
                    # print(f'result options {i} {j}: {options}')
                    nextCell.options = options
                    nextTiles.append(nextCell)
        
        grid = nextTiles
    # print(nextTiles)



pygame.quit()
   