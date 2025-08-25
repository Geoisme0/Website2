# main.py
import pygame
import sys
from settings import WIDTH, HEIGHT, FPS
from game import Game
from ui import draw_main_menu, draw_game_over

def main_loop():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Last Floor Standing: Solo Run")
    clock = pygame.time.Clock()

    state = "menu"
    game = Game(screen)

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if state == "menu" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.reset()
                    state = "game"

            elif state == "gameover" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.reset()
                    state = "game"

            elif state == "game":
                game.handle_event(event)

        if state == "menu":
            draw_main_menu(screen)
        elif state == "game":
            game.update()
            if game.game_over:
                state = "gameover"
        elif state == "gameover":
            draw_game_over(screen, game.floors_climbed)
