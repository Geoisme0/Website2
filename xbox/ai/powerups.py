# powerups.py
import pygame
import random
from settings import WIDTH

def spawn_powerup(powerups, camera_y_offset):
    kind = random.choice(["jetpack", "slowlava"])
    powerups.append({
        "rect": pygame.Rect(random.randint(100, WIDTH - 100), camera_y_offset - random.randint(100, 400), 20, 20),
        "type": kind
    })

def apply_powerup(player, lava, pu_type):
    if pu_type == "jetpack":
        player.has_jetpack = True
        player.jetpack_fuel = 100
    elif pu_type == "slowlava":
        lava.slowdown = 0.5
