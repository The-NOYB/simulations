import pygame as pg
import random, sys, math
from block import Block

pg.init()
window = pg.display.set_mode((900,900))
clock = pg.time.Clock()

path = []
visited = []
maze = []
leng = 10    # 3x3 grid for now

# special color for the visited block
visited_surf = pg.Surface( (30,30) )
visited_surf.fill( (100, 50, 100) )

# the backtracking algorithm
def algorithm( maze, block, path, visited, feedback):

    visited.append( block.index )
    # left, right, up, down
    choices = [-1, 1, -leng, leng]
    removal_list = []

    # remove the directions which connect to visited nodes or are not connected 
    for choice in choices:
        # edge cases
        if (choice == 1 and block.position[1] == leng-1):
            removal_list.append(choice)
        elif (choice == -1 and block.position[1] == 0):
            removal_list.append(choice)
        elif (choice == -leng and block.position[0] == 0):
            removal_list.append(choice)
        elif (choice == leng and block.position[0] == leng-1):
            removal_list.append(choice)
        # if the node is visited
        elif ((block.index + choice) in visited):
            removal_list.append(choice)
        elif ( choice == feedback):
            removal_list.append(choice)

    for i in removal_list:
        choices.remove(i)

    # getting the wrong block
    if not choices:
        last_block = visited.pop()
        feedback = last_block - visited[-1]
        return maze[ visited[-1] ], feedback

    direction_choosen = random.choice(choices)
    print( f"{direction_choosen = }, {block.index = }" )
    block_choosen = maze[block.index + direction_choosen]

    if direction_choosen == 1:
        block.right = True
        block_choosen.left = True
    elif direction_choosen == -1:
        block.left = True
        block_choosen.right = True
    elif direction_choosen == -leng:
        block.up = True
        block_choosen.down = True
    else:
        block.down = True
        block_choosen.up = True

    return block_choosen, feedback

# making a grid
maze = [ Block(index, leng) for index in range(leng**2) ]

# making a random block the start
startBlock = maze[ random.randrange(leng**2) ]
startBlock.isStart = True

current_block = startBlock
feedback = 0

for i in range( leng**2 ):
    maze[i].make_img()

while True:
    window.fill( (100,100,100) )

    current_block, feedback = algorithm(maze, current_block, path, visited, feedback)

#    # drawing the maze
    for block in  maze:
        window.blit( block.surf, block.rect.topleft)
    
    for visited_block in visited:
        _pos = block.rect.width * maze[visited_block].position[0], block.rect.width * maze[visited_block].position[1]
        window.blit( visited_surf, _pos )

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    pg.display.update()
    clock.tick(5)
