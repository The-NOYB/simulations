import pygame, math, random, sys, time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animated Radar Simulation")
clock = pygame.time.Clock()

# Radar origin (bottom-left corner)
RADAR_ORIGIN = (0, HEIGHT)

# Constants
NUM_TARGETS = 20
RAY_STEP = 4 # assume 4x =  1000m/s
MAX_DISTANCE = 1500
RAY_SPACING_DEG = 1

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Generate random targets (x, y, radius)
TARGETS = [
    (random.randint(100, WIDTH - 50), random.randint(100, HEIGHT - 50), 10)
    for _ in range(NUM_TARGETS)
]

# Define ray structure: each ray has angle, current length, and hit info
def update_results(rays, result_rays):
    for ray in rays:
        if ray.reached_origin:
            distance = 100//4*(ray.length_front + ray.length_back)//2
            time = distance / 3e8
            result_rays[ray.index] = "{}Km covered in {}s".format(distance, time)


class RadarRay:
    def __init__(self, angle_deg):
        self.index = angle_deg
        self.angle = math.radians(angle_deg)
        self.length_front= 0
        self.length_back= 0
        self.hit_point = None
        self.reached_origin = False
        self.hit = False
        self.stop = False
        self.distance = 0

    def update(self):
        if self.hit and not self.reached_origin:
            self.length_back += RAY_STEP
            dx = -math.cos(self.angle) * self.length_back
            dy = math.sin(self.angle) * self.length_back 
    
            x = self.hit_point[0] + dx
            y = self.hit_point[1] + dy

            if x <= 0 and y >= HEIGHT:
                self.reached_origin = True
                return

        elif not self.stop:
            self.length_front += RAY_STEP
            dx = math.cos(self.angle) * self.length_front
            dy = -math.sin(self.angle) * self.length_front 
    
            x = RADAR_ORIGIN[0] + dx
            y = RADAR_ORIGIN[1] + dy
    
            if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or self.length_front > MAX_DISTANCE:
                self.stop = True  # Mark as done if out of bounds
                return
    
            for tx, ty, radius in TARGETS:
                if math.hypot(x - tx, y - ty) < radius:
                    self.hit = True
                    self.hit_point = (x, y)
                    break

    def draw(self, surface):
        if self.hit and not self.reached_origin:
            dx = -math.cos(self.angle) * self.length_back
            dy = math.sin(self.angle) * self.length_back
            x = self.hit_point[0] + dx
            y = self.hit_point[1] + dy

            pygame.draw.line(surface, RED, RADAR_ORIGIN, self.hit_point, 1)
            pygame.draw.line(surface, BLUE, self.hit_point, (x, y), 2)
        elif self.reached_origin:
            pygame.draw.line(surface, BLUE, RADAR_ORIGIN, self.hit_point, 2)
        else:
            dx = math.cos(self.angle) * self.length_front
            dy = -math.sin(self.angle) * self.length_front
            x = RADAR_ORIGIN[0] + dx
            y = RADAR_ORIGIN[1] + dy

            pygame.draw.line(surface, RED, RADAR_ORIGIN, (x, y), 1)

# Create rays in all directions
rays = [RadarRay(angle) for angle in range(0, 90, RAY_SPACING_DEG)]

result_rays = {}

# Main loop
running = True
while running:
    clock.tick(60)
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw radar origin
    pygame.draw.circle(screen, GREEN, RADAR_ORIGIN, 5)

    # Draw targets
    for tx, ty, r in TARGETS:
        pygame.draw.circle(screen, WHITE, (tx, ty), r)

    # Update and draw rays
    for ray in rays:
        ray.update()
        ray.draw(screen)
        update_results(rays, result_rays)

    for result in result_rays:
        print(result_rays[result])
    pygame.display.flip()

pygame.quit()
sys.exit()

