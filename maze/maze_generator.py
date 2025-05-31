import pygame as pg
import random, sys, math
from block import Block

pg.init()
window = pg.display.set_mode((900,900))
clock = pg.time.Clock()

path = []
maze = []
leng = 10    # 3x3 grid for now

# special color for the visited block
visited_surf = pg.Surface( (30,30) )
visited_surf.fill( (100, 50, 100) )

# the backtracking algorithm
def gen_algorithm( maze, path ):

    if not path:
        return None

    block = path.pop()
    block.visited = True

    # left, right, up, down
    # wtf it is up, down, left, right, no idea bruh
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
        elif maze[block.index + choice].visited :
            removal_list.append(choice)
#        elif ( choice == feedback):
#            removal_list.append(choice)

    for i in removal_list:
        choices.remove(i)

    # getting the wrong block
    if not choices and not path:
        block.isEnd = True
        block.make_img()
        print(f"{block.index, block.isStart, block.isEnd}")
        return None
    elif not choices:
        return block

    path.append(block)
    direction_choosen = random.choice(choices)
    block_choosen = maze[block.index + direction_choosen]
    block_choosen.visited = True

    if direction_choosen == 1:
        block.down = True
        block_choosen.up = True
#        print("down")
    elif direction_choosen == -1:
        block.up = True
        block_choosen.down = True
#        print("up")
    elif direction_choosen == -leng:
        block.left = True
        block_choosen.right = True
#        print("left")
    else:
        block.right = True
        block_choosen.left = True
#        print("right")

    block.make_img()
    block_choosen.make_img()

    path.append(block_choosen)
    return block_choosen

def init_maze():
    global maze, path
    # making a grid
    maze = [ Block(index, leng) for index in range(leng**2) ]
    
    # the custom start, end and step is for starting being in border only
    start, end, step = random.choice( [ (0, leng, 1), (0, leng**2, leng), (leng-1, leng**2, leng), ((leng-1)*leng, leng**2, 1)]  )

    # making the random border block the startBlock
    startBlock = maze[ random.randrange( start, end, step ) ]
    startBlock.isStart = True
    path.append(startBlock)

init_maze()
current_block = path[-1]

while True:
    window.fill( (0,100,100) )

    if not current_block:
        pg.time.wait(5000)
        init_maze()
    current_block = gen_algorithm(maze, path)

#    # drawing the maze
    for block in maze:
#        if block.visited:
        if block == current_block:
            _pos = block.rect.width * block.position[0], block.rect.width * block.position[1]
            window.blit( visited_surf, _pos )
        else:
            window.blit( block.surf, block.rect.topleft)
    
#    for visited_block in visited:
#        _pos = block.rect.width * maze[visited_block].position[0], block.rect.width * maze[visited_block].position[1]
#        window.blit( visited_surf, _pos )

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    pg.display.update()
    clock.tick(4)
