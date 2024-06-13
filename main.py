import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Get display info
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h

# Constants for the game
WIDTH, HEIGHT = min(SCREEN_WIDTH, 1000), min(SCREEN_HEIGHT, 800)  # Adjusted to fit within screen bounds
PLAYER_WIDTH, PLAYER_HEIGHT = 40, 60
PLAYER_VEL = 5
STAR_RADIUS = 15
STAR_VEL = 3
STAR_ACCELERATION = 0.1
BULLET_VEL = 7
BULLET_WIDTH, BULLET_HEIGHT = 5, 10

# Load resources
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SHOOTING STAR")
BG = pygame.transform.scale(pygame.image.load("bg.jpeg"), (WIDTH, HEIGHT))
FONT = pygame.font.SysFont("comicsans", 30)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
RED_GRADIENT = [(255, 0, 0), (255, 100, 100), (255, 150, 150), (255, 200, 200)]  # Gradient of red colors

# Functions for the game
def draw_player_icon(x, y):
    # Create a surface for the player icon
    player_surface = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)

    # Draw the polygon with gradient effect
    for i, color in enumerate(RED_GRADIENT):
        pygame.draw.polygon(player_surface, color,
                            [(PLAYER_WIDTH // 2, i * (PLAYER_HEIGHT // len(RED_GRADIENT))),
                             (0, PLAYER_HEIGHT),
                             (PLAYER_WIDTH, PLAYER_HEIGHT)])

    # Blit the player surface onto the game window
    WIN.blit(player_surface, (x, y))

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    WIN.blit(text_surface, (x, y))

def main_menu():
    clock = pygame.time.Clock()
    title_text = FONT.render("SHOOTING STAR", True, WHITE)
    start_text = FONT.render("Press S to Start or Q to Quit", True, WHITE)
    animate_text = FONT.render("Press SPACE to Shoot and ARROW keys to move", True, WHITE)
    

    show_animation_text = False
    menu_running = True

    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return "start"
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        WIN.blit(BG, (0, 0))

        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 100))
        draw_player_icon(WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT // 2)
        WIN.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 100))

        if show_animation_text:
            WIN.blit(animate_text, (WIDTH // 2 - animate_text.get_width() // 2, HEIGHT - 50))
        
        pygame.display.update()
        clock.tick(60)

        if pygame.time.get_ticks() % 2000 > 1000:
            show_animation_text = True
        else:
            show_animation_text = False

def draw_game_over(score):
    WIN.fill((0, 0, 0))
    lost_text = FONT.render("Game Over!", True, WHITE)
    score_text = FONT.render(f"Final Score: {score}", True, WHITE)
    menu_text = FONT.render("Press M for Main Menu or Q to Quit", True, WHITE)
    
    WIN.blit(lost_text, (WIDTH//2 - lost_text.get_width()//2, HEIGHT//2 - lost_text.get_height()//2 - 40))
    WIN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - score_text.get_height()//2))
    WIN.blit(menu_text, (WIDTH//2 - menu_text.get_width()//2, HEIGHT//2 - menu_text.get_height()//2 + 40))
    
    pygame.display.update()

def main():
    while True:
        main_menu()
        run_game()

def run_game():
    player_rect = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks() / 1000
    star_add_increment = 2000
    star_count = 0
    stars = []
    bullets = []
    star_vel = STAR_VEL

    while True:
        elapsed_time = (pygame.time.get_ticks() / 1000) - start_time
        score = round(elapsed_time * 10)

        handle_input(player_rect, bullets)
        game_over = handle_stars(stars, star_vel, player_rect, bullets)
        handle_bullets(bullets)
        draw_game(player_rect, stars, bullets, score)

        if game_over:
            break

        star_count += clock.tick(60)
        if star_count > star_add_increment:
            add_stars(stars)
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0
            star_vel += STAR_ACCELERATION

    handle_game_over(score)

def handle_input(player_rect, bullets):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.x - PLAYER_VEL >= 0:
        player_rect.x -= PLAYER_VEL
    if keys[pygame.K_RIGHT] and player_rect.x + PLAYER_VEL + player_rect.width <= WIDTH:
        player_rect.x += PLAYER_VEL
    if keys[pygame.K_UP] and player_rect.y - PLAYER_VEL >= 0:
        player_rect.y -= PLAYER_VEL
    if keys[pygame.K_DOWN] and player_rect.y + PLAYER_VEL + player_rect.height <= HEIGHT:
        player_rect.y += PLAYER_VEL

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(pygame.Rect(player_rect.x + player_rect.width//2 - BULLET_WIDTH//2, player_rect.y, BULLET_WIDTH, BULLET_HEIGHT))

def handle_stars(stars, star_vel, player_rect, bullets):
    for star in stars[:]:
        star.y += star_vel
        if star.y > HEIGHT:
            stars.remove(star)
        elif player_rect.colliderect(star):
            return True  # Game over condition if player collides with a star

        for bullet in bullets[:]:
            if star.colliderect(bullet):
                stars.remove(star)
                bullets.remove(bullet)
    return False

def handle_bullets(bullets):
    for bullet in bullets[:]:
        bullet.y -= BULLET_VEL
        if bullet.y < 0:
            bullets.remove(bullet)

def add_stars(stars):
    for _ in range(3):
        star_x = random.randint(STAR_RADIUS, WIDTH - STAR_RADIUS)
        star_y = -STAR_RADIUS
        stars.append(pygame.Rect(star_x, star_y, STAR_RADIUS*2, STAR_RADIUS*2))

def draw_game(player_rect, stars, bullets, score):
    WIN.blit(BG, (0, 0))
    draw_text(f"Time: {round(pygame.time.get_ticks() / 1000)}s", FONT, WHITE, 10, 10)
    draw_text(f"Score: {score}", FONT, WHITE, 10, 40)
    draw_player_icon(player_rect.x, player_rect.y)
    for star in stars:
        # Draw stars with gradient of red colors
        pygame.draw.circle(WIN, RED_GRADIENT[0], (star.x, star.y), STAR_RADIUS)
    for bullet in bullets:
        pygame.draw.rect(WIN, RED, bullet)
    pygame.display.update()

def handle_game_over(score):
    while True:
        draw_game_over(score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    return  # Go back to main menu
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main()
