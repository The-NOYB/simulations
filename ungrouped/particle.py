import pygame as pg
import math

class Particle(pg.sprite.Sprite):
    def __init__(self, type, mass, vector, pos):
        super().__init__()
        self.type = type
        self.mass = mass * 1000     # kgs to grams lmao
        self.vector = vector
        self.leng = self.form()
        self.make_img()
        self.rect.x, self.rect.y = pos
        self.collided = False

    def form(self):
        if self.type == "circle":
            return 2 * math.sqrt(self.mass / math.pi)
        elif self.type == "square":
            return math.sqrt(self.mass)
        elif self.type == "triangle":
            return math.sqrt( self.mass * 4 / math.sqrt(3) )
    
    def draw(self, screen):
         screen.blit( self.image, (self.x, self.y) )
        
    def update(self):
        dx = self.rect.x + self.vector.x
        dy = self.rect.y + self.vector.y

        if (dx > 0 and (dx + self.leng) < 800):
            self.rect.x = dx
        else:
            self.vector.x *= -1

        if (dy > 0 and (dy + self.leng) < 600):
            self.rect.y = dy
        else:
            self.vector.y *= -1

    def make_img(self):
        if self.type == "circle":
            self.image = pg.Surface( (self.leng, self.leng) )
            pg.draw.circle( self.image, (158, 200, 50), (self.leng//2,)*2, self.leng//2 )
            self.image.set_colorkey( (0,0,0) )
            self.rect = self.image.get_rect()
        elif self.type == "square":
            self.image = pg.Surface( (self.leng, self.leng) )
            self.image.fill( (158, 200, 50) )
            self.rect = self.image.get_rect()
        elif self.type == "triangle":
            self.image = pg.Surface( (self.leng, self.leng) )
            angle = math.radians(60)
            pg.draw.polygon( self.image, (158, 200, 50), [ (0, self.leng), (self.leng, self.leng), (self.leng//2, 0) ] )
            self.image.set_colorkey( (0,0,0) )
            self.rect = self.image.get_rect()
