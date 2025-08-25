import pygame
import sys
import random

# === Setup ===
pygame.init()
WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Last Floor Standing: Solo Run")
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("consolas", 28)

# === Colors ===
RED = (200, 30, 30)
WHITE = (255, 255, 255)
GREEN = (50, 255, 50)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 50)
BLUE = (50, 150, 255)

# === Constants ===
GRAVITY = 0.7
JUMP_POWER = -13
MOVE_SPEED = 6
MAX_VERTICAL_GAP = 150
MAX_HORIZONTAL_GAP = 250

# === State ===
state = "menu"

# === Entities ===
player = pygame.Rect(0, 0, 40, 40)
player_speed_y = 0
coyote_time = 0
jump_buffer = 0
has_jetpack = False
jetpack_fuel = 100
lava_y = HEIGHT
lava_speed = 0.25
lava_slowdown = 1.0
floors_climbed = 0
camera_y = 0
platforms = []
powerups = []

def reset_game():
    global player, player_speed_y, coyote_time, jump_buffer, has_jetpack, jetpack_fuel
    global lava_y, lava_speed, lava_slowdown, floors_climbed, camera_y, platforms, powerups

    player_speed_y = 0
    coyote_time = 0
    jump_buffer = 0
    has_jetpack = False
    jetpack_fuel = 100
    lava_y = HEIGHT
    lava_speed = 0.25
    lava_slowdown = 1.0
    floors_climbed = 0
    camera_y = 0
    powerups = []

    base = pygame.Rect(550, 600, 180, 20)
    platforms = [base]
    player.x = base.x + base.width // 2 - player.width // 2
    player.y = base.y - player.height

    for _ in range(5):
        last = platforms[-1]
        new_x = last.x + random.randint(-MAX_HORIZONTAL_GAP, MAX_HORIZONTAL_GAP)
        new_y = last.y - random.randint(80, MAX_VERTICAL_GAP)
        new_x = max(40, min(new_x, WIDTH - 160))
        platforms.append(pygame.Rect(new_x, new_y, 120, 20))

def draw_ui():
    score = FONT.render(f"Floors Climbed: {floors_climbed}", True, WHITE)
    SCREEN.blit(score, (20, 20))
    if has_jetpack:
        jp = FONT.render(f"Jetpack: {int(jetpack_fuel)}%", True, YELLOW)
        SCREEN.blit(jp, (WIDTH - jp.get_width() - 20, 20))

def spawn_powerup(x, y):
    kind = random.choice(["jetpack", "slowlava"])
    powerups.append({"rect": pygame.Rect(x, y, 20, 20), "type": kind})

def main_menu():
    SCREEN.fill(BLACK)
    title = FONT.render("Last Floor Standing: Solo Run", True, WHITE)
    prompt = FONT.render("Press [SPACE] to Start", True, YELLOW)
    SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 60))
    SCREEN.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2))
    pygame.display.flip()

def game_over_screen():
    SCREEN.fill(BLACK)
    text = FONT.render("🔥 You Got Burned! Game Over 🔥", True, RED)
    score = FONT.render(f"You climbed {floors_climbed} floors", True, WHITE)
    prompt = FONT.render("Press [SPACE] to Restart", True, YELLOW)
    SCREEN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 60))
    SCREEN.blit(score, (WIDTH//2 - score.get_width()//2, HEIGHT//2))
    SCREEN.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 + 60))
    pygame.display.flip()

def game_loop():
    global player_speed_y, coyote_time, jump_buffer, has_jetpack, jetpack_fuel
    global lava_y, lava_speed, lava_slowdown, floors_climbed, camera_y, state

    keys = pygame.key.get_pressed()

    # Move left/right
    if keys[pygame.K_LEFT]:
        player.x -= MOVE_SPEED
    if keys[pygame.K_RIGHT]:
        player.x += MOVE_SPEED

    # Jump buffer
    if keys[pygame.K_SPACE]:
        jump_buffer = 10

    jump_buffer -= 1
    coyote_time -= 1

    # Jetpack handling
    if has_jetpack and keys[pygame.K_SPACE] and jetpack_fuel > 0:
        player_speed_y = -8
        jetpack_fuel -= 1
    else:
        player_speed_y += GRAVITY

    player.y += player_speed_y

    # Platform collision & coyote time reset
    on_ground = False
    for plat in platforms:
        if player.colliderect(plat) and player_speed_y > 0 and player.bottom <= plat.bottom + 10:
            player.bottom = plat.top
            player_speed_y = 0
            coyote_time = 10
            on_ground = True

    # Jump if buffered and coyote time
    if jump_buffer > 0 and coyote_time > 0:
        player_speed_y = JUMP_POWER
        jump_buffer = 0

    # Camera smoothly follows player
    camera_target = player.y - HEIGHT // 2
    camera_y += (camera_target - camera_y) * 0.1

    # Check death by lava contact
    if player.bottom > lava_y:
        state = "gameover"

    # Lava rises
    lava_y -= lava_speed * lava_slowdown
    lava_speed += 0.0005

    # Spawn powerups randomly above camera view
    if random.random() < 0.1:
        spawn_powerup(random.randint(100, WIDTH - 100), camera_y - random.randint(100, 400))

    # Increment floors climbed when player moves upward past camera_y
    if player.y < camera_y:
        floors_climbed += 1

    # Remove platforms BELOW the lava line (so platforms under lava disappear)
    platforms[:] = [p for p in platforms if p.y + p.height > lava_y]

    # Ensure platforms spawn *above* camera y by at least 10px to keep the challenge
    while True:
        if len(platforms) >= 10:
            break
        last = platforms[-1]
        # Make new platform at least 10 pixels above camera_y, but also above last platform
        min_y = min(last.y - random.randint(80, MAX_VERTICAL_GAP), camera_y - 10)
        new_y = min_y
        new_x = last.x + random.randint(-MAX_HORIZONTAL_GAP, MAX_HORIZONTAL_GAP)
        new_x = max(40, min(new_x, WIDTH - 160))
        platforms.append(pygame.Rect(new_x, new_y, 120, 20))

    # Player collects powerups
    for pu in powerups[:]:
        if player.colliderect(pu["rect"]):
            if pu["type"] == "jetpack":
                has_jetpack = True
                jetpack_fuel = 100
            elif pu["type"] == "slowlava":
                lava_slowdown = 0.5
            powerups.remove(pu)

    # --- Drawing ---
    SCREEN.fill(BLACK)

    # Draw lava (rising rectangle)
    pygame.draw.rect(SCREEN, RED, (0, lava_y - camera_y, WIDTH, HEIGHT))

    # Draw platforms
    for plat in platforms:
        pygame.draw.rect(SCREEN, WHITE, (plat.x, plat.y - camera_y, plat.width, plat.height))

    # Draw powerups
    for pu in powerups:
        color = BLUE if pu["type"] == "slowlava" else YELLOW
        pygame.draw.rect(SCREEN, color, (pu["rect"].x, pu["rect"].y - camera_y, pu["rect"].width, pu["rect"].height))

    # Draw player
    pygame.draw.rect(SCREEN, GREEN, (player.x, player.y - camera_y, player.width, player.height))

    # Draw UI
    draw_ui()

    pygame.display.flip()

reset_game()

while True:
    CLOCK.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if state == "menu":
        main_menu()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            reset_game()
            state = "game"

    elif state == "game":
        game_loop()

    elif state == "gameover":
        game_over_screen()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            reset_game()
            state = "game"
