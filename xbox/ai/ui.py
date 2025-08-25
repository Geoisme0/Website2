# ui.py
import pygame
from settings import FONT, WHITE, YELLOW, RED, BLACK

def draw_ui(screen, player, floors_climbed, paused):
    score_text = FONT.render(f"Floors Climbed: {floors_climbed}", True, WHITE)
    screen.blit(score_text, (20, 20))

    if player.has_jetpack:
        fuel = FONT.render(f"Jetpack: {int(player.jetpack_fuel)}%", True, YELLOW)
        screen.blit(fuel, (screen.get_width() - fuel.get_width() - 20, 20))

    if paused:
        pause = FONT.render("PAUSED", True, RED)
        screen.blit(pause, (screen.get_width() // 2 - pause.get_width() // 2, 100))

def draw_main_menu(screen):
    screen.fill(BLACK)
    title = FONT.render("Last Floor Standing: Solo Run", True, WHITE)
    prompt = FONT.render("Press [SPACE] to Start", True, YELLOW)
    screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, screen.get_height() // 2 - 60))
    screen.blit(prompt, (screen.get_width() // 2 - prompt.get_width() // 2, screen.get_height() // 2))
    pygame.display.flip()

def draw_game_over(screen, floors_climbed):
    screen.fill(BLACK)
    text = FONT.render("🔥 You Got Burned! Game Over 🔥", True, RED)
    score = FONT.render(f"You climbed {floors_climbed} floors", True, WHITE)
    prompt = FONT.render("Press [SPACE] to Restart", True, YELLOW)
    screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - 60))
    screen.blit(score, (screen.get_width() // 2 - score.get_width() // 2, screen.get_height() // 2))
    screen.blit(prompt, (screen.get_width() // 2 - prompt.get_width() // 2, screen.get_height() // 2 + 60))
    pygame.display.flip()
