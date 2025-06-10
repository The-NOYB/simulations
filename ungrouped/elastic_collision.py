import pygame as pg
import random, sys, math, time
from particle import Particle

pg.init()
window = pg.display.set_mode((800,600))
clock = pg.time.Clock()

circle = Particle("circle", 4, pg.math.Vector2(2, 5), (100, 100))
triangle = Particle("triangle", 3, pg.math.Vector2(-3, 2), (100, 200))
square = Particle("square", 8, pg.math.Vector2(4, 2), (200, 100))

circles = pg.sprite.Group()
squares = pg.sprite.Group()
triangles = pg.sprite.Group()
collide = True
collide_time = 0

circles.add( circle )
triangles.add( triangle )
squares.add( square )

def check_collision( circles, squares, triangles ):
    for circle in circles:
        result = pg.sprite.spritecollideany(circle, squares)
        if result and pg.sprite.collide_mask(circle, result) and not (circle.collided or result.collided):
            circle.collided = True
            result.collided = True
            ellastic_collide(result, circle)
        elif result:
            circle.collided = False
            result.collided = False

        result = pg.sprite.spritecollideany(circle, triangles)
        if result and pg.sprite.collide_mask(circle, result) and not (circle.collided or result.collided):
            circle.collided = True
            result.collided = True
            ellastic_collide(result, circle)
        elif result:
            circle.collided = False
            result.collided = False

    for square in squares:
        result = pg.sprite.spritecollideany(square, triangles)
        if result and pg.sprite.collide_mask(square, result) and not (square.collided or result.collided):
            square.collided = True
            result.collided = True
            ellastic_collide(result, square)
        elif result:
            square.collided = False
            result.collided = False

def ellastic_collide( particle1, particle2 ):
    global collide, collide_time
    m1 = particle1.mass
    m2 = particle2.mass
    v1 = particle1.vector
    v2 = particle2.vector

    rel_velocity = (v1-v2)
    direction = (pg.math.Vector2(particle1.rect.center) - pg.math.Vector2(particle2.rect.center)).normalize()

    v3 =  v1 + 2 * m2 / (m1 + m2) * (-rel_velocity).dot(-direction) * -direction
    v4 =  v2 + 2 * m1 / (m1 + m2) * (rel_velocity).dot(direction) * (direction)

    print(v1, v2, v3, v4)
    collide = False
    collide_time = time.time()

    particle1.vector = v3
    particle2.vector = v4

while True:
    window.fill( (100,100,100) )

    check_collision( circles, squares, triangles )

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
    clock.tick(60)
