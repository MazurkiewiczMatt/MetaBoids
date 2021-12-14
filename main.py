import random
import numpy as np
from PIL import Image, ImageDraw
import pygame
import sys

SCALE = 10
size = 500
bsize = size / 35
c = size / SCALE
dt = 0.1


def initialize_boid():
    return [random.random() * SCALE, random.random() * SCALE, 1, random.random() * 2 * np.pi]


def initialize(N=10):
    state = []
    for i in range(N):
        state.append(initialize_boid())
    return np.array(state)


state = initialize()


def update(state):
    s = np.transpose(state)
    s[0] = s[0] + s[2] * np.cos(s[3]) * dt
    s[1] = s[1] + s[2] * np.sin(s[3]) * dt
    return np.transpose(s)

def check_if_close(index, state, radius=bsize/c, bounds=(SCALE, SCALE)):
    for i in range(len(state)):
        if state[index][0] > SCALE or state[index][1] > SCALE or state[index][0] < 0 or state[index][1] < 0:
            return 1
        if i != index:
            if (state[i][0]-state[index][0])**2 + (state[i][1]-state[index][1])**2 < radius**2:
                return 1

    return 0

def loss(rule):
    sum_dead = []
    for n in range(20):
        state = initialize(10)
        dead = np.zeros(len(state))
        for i in range(200):
            state = rule(state)
            state = update(state)
            for j in range(len(state)):
                if dead[j] == 0:
                    dead[j] = check_if_close(j, state)
        sum_dead.append(np.sum(dead))

    return sum_dead



pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))

print(loss(lambda x : x))

# Game loop.
while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    state = update(state)

    for boid in state:
        point1 = (boid[0] * c + bsize * np.cos(boid[3]), boid[1] * c + bsize * np.sin(boid[3]))
        point2 = (boid[0] * c + bsize * np.cos(boid[3] + 2.5), boid[1] * c + bsize * np.sin(boid[3] + 2.5))
        point3 = (boid[0] * c + bsize * np.cos(boid[3] - 2.5), boid[1] * c + bsize * np.sin(boid[3] - 2.5))
        pygame.draw.polygon(screen, 'red', [point1, point2, point3])

    pygame.display.flip()
    fpsClock.tick(fps)



