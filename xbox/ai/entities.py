# entities.py
import pygame
from settings import GRAVITY, JUMP_POWER

class Player:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 40, 40)
        self.vel_y = 0
        self.coyote_time = 0
        self.jump_buffer = 0
        self.has_jetpack = False
        self.jetpack_fuel = 100

    def jump(self):
        if self.jump_buffer > 0 and self.coyote_time > 0:
            self.vel_y = JUMP_POWER
            self.jump_buffer = 0

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= 6
        if keys[pygame.K_RIGHT]:
            self.rect.x += 6
        if keys[pygame.K_SPACE]:
            self.jump_buffer = 10

        self.jump_buffer -= 1
        self.coyote_time -= 1

        if self.has_jetpack and keys[pygame.K_SPACE] and self.jetpack_fuel > 0:
            self.vel_y = -8
            self.jetpack_fuel -= 1
        else:
            self.vel_y += GRAVITY

        self.rect.y += self.vel_y

class Lava:
    def __init__(self, start_y):
        self.y = start_y
        self.speed = 0.25
        self.slowdown = 1.0

    def update(self):
        self.y -= self.speed * self.slowdown
        self.speed += 0.0005
