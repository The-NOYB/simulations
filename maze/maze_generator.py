import random
import pygame as pg
import sys

pg.init()
window = pg.display.set_mode((900,900))
pg.display.set_caption("Test client")
clock = pg.time.Clock()

path = []
visited = []    # you could make isivisited a property of the class so that there is no need to look for cell in a list
maze = []
leng = 30    # 3x3 grid for now

visited_surf = pg.Surface( (30,30) )
visited_surf.fill( (100, 50, 100) )

# just the calling function
def solve ( maze, block, path, visited ):
    visited.append(block)

    algorithm(maze, block, path, visited)

# the backtracking algorithm
def algorithm( maze, block, path, visited ):

    # left, right, up, down
    choices = [-1,1,-leng,leng]
    removal_list = []

    # remove the directions which connect to visited nodes or are not connected 
    for i in choices:
        if ( block + i < 0 or block + i >= leng: )
            removal_list.append(i)
        elif ( (block + i) in visited ):
            removal_list.append(i)

    for i in removal_list:
        choices.remove(i)

    direction_choosen = block + random.choice( choices )


class Block():
    def __init__(self, index, left=False, right=False, up=False, down=False):
        self.isstart = False
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.isend = False
        self.position = [ index%leng, index//leng ]
        self.rect = pg.Rect(0,0,30,30)
        self.surf = pg.Surface( (30,30) )
        self.surf.fill( (0,0,0) )

    def make_img(self):
        # assigning the correct coords to each nodes change 3 according to sidexside maze
        self.rect.x = self.position[0] * 30
        self.rect.y = self.position[1] * 30
        
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
            pg.draw.circle( self.surf, (0,255,0), (14,14), 3)

# making a grid
for index in range(900):
    block = Block( index )
    block.make_img()
    maze.append( block )

# making a random block the start
choice = random.choice( maze )
choice.isstart = True

while True:
    window.fill( (100,100,100) )

#    # drawing the maze
    for block in  maze:
        window.blit( block.surf, block.rect.topleft)
    
    for visited_block in visited:
        window.blit( visited_surf, maze[visited_block].rect.topleft )

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    pg.display.update()
    clock.tick(60)
