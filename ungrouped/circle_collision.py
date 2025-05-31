import pygame as pg
import random, sys, math
from particle import Particle

pg.init()
window = pg.display.set_mode((800,600))
clock = pg.time.Clock()

circle = Particle("circle", 5, pg.math.Vector2(2, 2), (100, 100))
#triangle = Particle("triangle", 5, pg.math.Vector2(-3, 2), (100, 200))
square = Particle("square", 5, pg.math.Vector2(1, 3), (200, 100))

circles = pg.sprite.Group()
squares = pg.sprite.Group()
triangles = pg.sprite.Group()

circles.add( circle )
#triangles.add( triangle )
squares.add( square )

def check_collision( circles, squares, triangles ):

    sq_tri = pg.sprite.groupcollide(squares, triangles, False, False)
    cir_tri = pg.sprite.groupcollide(circles, triangles, False, False)
    cir_sq = pg.sprite.groupcollide(circles, squares, False, False)

while True:
    window.fill( (100,100,100) )

#    check_collision( circles, squares, triangles )

    for circle in circles:
        result = pg.sprite.spritecollideany(circle, squares)
        if result and pg.sprite.collide_mask(circle, result):
            circle.collided = True
            result.collided = True

        result = pg.sprite.spritecollideany(circle, triangles)
        if result and pg.sprite.collide_mask(circle, result):
            circle.collided = True
            result.collided = True

    for square in squares:
        result = pg.sprite.spritecollideany(square, triangles)
        if result and pg.sprite.collide_mask(square, result):
            square.collided = True
            result.collided = True

    circles.update()
    circles.draw( window )

    triangles.update()
    triangles.draw( window )

    squares.update()
    squares.draw( window )

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    pg.display.update()
    clock.tick(120)
