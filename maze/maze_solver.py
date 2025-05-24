import random
import pygame as pg
import sys

pg.init()
window = pg.display.set_mode((900,900))
pg.display.set_caption("Test client")
clock = pg.time.Clock()

path = []
visited = []
maze = []
leng = 3    # 3x3 grid for now

# just the calling function
def solve ( maze, block, path, visited ):
    path.append(block)
    visited.append(block)

    algorithm(maze, block, path, visited)
    return path

# the backtracking algorithm
def algorithm( maze, block, path, visited ):

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

# the class for block which both saves data for directions and also makes the graphics
class Block():
    def __init__(self, left, right, up, down):
        self.isstart = False
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.isend = False
        self.rect = pg.Rect(0,0,30,30)
        self.surf = pg.Surface( (30,30) )
        self.surf.fill( (0,0,0) )

    def make_img(self, index, leng):
        # assigning the correct coords to each nodes change 3 according to sidexside maze
        self.rect.x = index%leng * 30
        self.rect.y = index//leng * 30
        
        # drawing walls for each node as white lines
        if not self.left:
            pg.draw.line( self.surf,(255,255,255),(0,0), (0,29))
        if not self.right and not self.isend:
            pg.draw.line( self.surf,(255,255,255),(29,0), (29,29))
        if not self.up:
            pg.draw.line( self.surf,(255,255,255),(0,0), (29,0))
        if not self.down:
            pg.draw.line( self.surf,(255,255,255),(0,29), (29,29))

        if self.isend:   # if end node then color it red
            pg.draw.circle( self.surf, (255,0,0), (14,14), 4)
        elif self.isstart:   # if start node then color it red
            pg.draw.circle( self.surf, (0,0,255), (14,14), 4)
        else:   # color it green
            pg.draw.circle( self.surf, (0,255,0), (14,14), 4)

# a very lengthy way of defining a maze yes.
# 0
block = Block(False, True, False, False)
maze.append( block )
# 1
block = Block(True, True, False, True)
block.isstart = True
maze.append( block )
# 2
block = Block(True, False, False, False)
block.isend = True
maze.append( block )
# 3
block = Block(False, True, False, False)
block.isend = True
maze.append( block )
# 4
block = Block(True, True, True, True)
maze.append( block )
# 5
block = Block(True, False, False, True)
maze.append( block )
# 6
block = Block(False, True, False, False)
maze.append( block )
# 7
block = Block(True, False, True, False)
maze.append( block )
# 8
block = Block(False, False, True, False)
maze.append( block )

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
