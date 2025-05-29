import random
import pygame as pg
import sys
from block import Block

pg.init()
window = pg.display.set_mode((900,900))
pg.display.set_caption("Test client")
clock = pg.time.Clock()

path = []
visited = []
maze = []
leng = 30   # 3x3 grid for now

# just the calling function
def solve ( maze, block, path, visited ):
    path.append(block)
    visited.append(block)

    solve_algorithm(maze, block, path, visited)
    return path

# the backtracking algorithm
def solve_algorithm( maze, block, path, visited ):

    if maze[block].isend:
        return 

    # left, right, up, down
    choices = [-1,1,-leng,leng]
    removal_list = []

    # remove the directions which connect to visited nodes or are not connected 
    for i in choices:
        if i==-1 and not maze[block].left :
            removal_list.append(i)
        elif i==1 and not maze[block].right :
            removal_list.append(i)
        elif i==-leng and not maze[block].up :
            removal_list.append(i)
        elif i==leng and not maze[block].down :
            removal_list.append(i)
        elif (block + i) in visited:
            removal_list.append(i)

    for i in removal_list:
        choices.remove(i)

    if choices:
        direction_choosen = choices[-1]  # choose the last option present in choice
        path.append( block + direction_choosen )
        visited.append( block + direction_choosen )
        algorithm( maze, block + direction_choosen, path, visited )
    else:
        path.pop()  # remove the current node
        algorithm( maze, path[-1], path, visited )  # go to the last node in path

# just calling the image functions
for index in range(len(maze)):
    maze[index].make_img(index, leng)

solve(maze, 8, path, visited )
print(path)

while True:
    window.fill( (100,100,100) )

    # drawing the maze
    for block in  maze:
        window.blit( block.surf, block.rect.topleft)

    # drawing the path lines
    for node in range(len(path)-1):
        start = path[node]
        end = path[node+1]
        start_pos = ( start%leng * 30 + 14, start//leng * 30 + 14 )
        end_pos = ( end%leng *30 + 14, end//leng * 30 + 14 )

        pg.draw.line( window, (0,255,0), start_pos, end_pos )

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    pg.display.update()
    clock.tick(60)
