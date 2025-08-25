# settings.py
import pygame

# Display
WIDTH = 1280
HEIGHT = 720
FPS = 60

# Colors
RED = (200, 30, 30)
WHITE = (255, 255, 255)
GREEN = (50, 255, 50)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 50)
BLUE = (50, 150, 255)
GREY = (100, 100, 100)
ORANGE = (255, 165, 0)

# Font
pygame.font.init()
FONT = pygame.font.SysFont("consolas", 28)

# Physics
GRAVITY = 0.7
JUMP_POWER = -13
MOVE_SPEED = 6

# Platform Generation
MAX_VERTICAL_GAP = 150
MAX_HORIZONTAL_GAP = 250
