import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game - Single Player AI")

# Colors
GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle and Ball setup
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
player = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ai = pygame.Rect(WIDTH - 60, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, 16, 16)

ball_speed = 5
ball_dx, ball_dy = ball_speed, ball_speed
paddle_speed = 7
ai_speed = 5

# Score
player_score = 0
ai_score = 0
font = pygame.font.SysFont(None, 48)
big_font = pygame.font.SysFont(None, 72)

# Clock
clock = pygame.time.Clock()

# Start screen
def start_screen():
    screen.fill(GREEN)
    title = big_font.render("PONG GAME", True, WHITE)
    prompt = font.render("Press SPACE to Start", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 100))
    screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2))
    pygame.display.flip()
    wait_for_space()

# Restart after score
def wait_for_space():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

# Draw score
def draw_score():
    score_text = font.render(f"{player_score}  :  {ai_score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

# Reset ball and paddles
def reset_positions():
    global ball_dx, ball_dy, ball_speed
    player.centery = HEIGHT // 2
    ai.centery = HEIGHT // 2
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed = 5
    ball_dx, ball_dy = ball_speed, ball_speed

# Game starts here
start_screen()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Input: Player 1 (left paddle)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player.top > 0:
        player.y -= paddle_speed
    if keys[pygame.K_DOWN] and player.bottom < HEIGHT:player.y += paddle_speed

    # AI Movement
    if ai.centery < ball.centery and ai.bottom < HEIGHT:
        ai.y += ai_speed
    if ai.centery > ball.centery and ai.top > 0:
        ai.y -= ai_speed

    # Ball movement
    ball.x += ball_dx
    ball.y += ball_dy

    # Bounce on top/bottom
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_dy *= -1

    # Paddle collisions
    if ball.colliderect(player) or ball.colliderect(ai):
        ball_dx *= -1
        ball_speed += 0.5  # increase speed each hit
        ball_dx = ball_speed if ball_dx > 0 else -ball_speed
        ball_dy = ball_speed if ball_dy > 0 else -ball_speed

    # Scoring
    if ball.left <= 0:
        ai_score += 1
        reset_positions()
        start_screen()
    elif ball.right >= WIDTH:
        player_score += 1
        reset_positions()
        start_screen()

    # Draw everything
    screen.fill(GREEN)
    pygame.draw.rect(screen, WHITE, player)
    pygame.draw.rect(screen, WHITE, ai)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
    draw_score()

    pygame.display.flip()
    clock.tick(60)
