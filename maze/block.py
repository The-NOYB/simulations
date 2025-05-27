import pygame as pg

class Block():
    def __init__(self, index, leng, left=False, right=False, up=False, down=False):
        self.isStart = False
        self.isEnd = False
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.index = index
        self.position = [ index//leng, index%leng ]
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
        if not self.right and not self.isEnd:
            pg.draw.line( self.surf,(255,255,255),(29,0), (29,29))
        if not self.up:
            pg.draw.line( self.surf,(255,255,255),(0,0), (29,0))
        if not self.down:
            pg.draw.line( self.surf,(255,255,255),(0,29), (29,29))

        if self.isEnd:   # if end node then color it red
            pg.draw.circle( self.surf, (255,0,0), (14,14), 4)
        elif self.isStart:   # if start node then color it red
            pg.draw.circle( self.surf, (0,0,255), (14,14), 4)
        else:   # color it green
            pg.draw.circle( self.surf, (0,255,0), (14,14), 3)
