import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle settings
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 70
PADDLE_SPEED = 5

# Ball settings
BALL_SIZE = 10
BALL_SPEED_X, BALL_SPEED_Y = 4, 4

# Power-up settings
POWERUP_SIZE = 15
POWERUP_RESPAWN_TIME = 5000  # milliseconds

# Game objects
player1 = pygame.Rect(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2 = pygame.Rect(WIDTH - 20, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 36)
score1 = 0
score2 = 0

# Power-up object
powerup_rect = pygame.Rect(
    random.randint(20, WIDTH - 20 - POWERUP_SIZE),
    random.randint(20, HEIGHT - 20 - POWERUP_SIZE),
    POWERUP_SIZE,
    POWERUP_SIZE,
)
powerup_visible = True
powerup_timer = 0

while True:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1.top > 0:
        player1.y -= PADDLE_SPEED
    if keys[pygame.K_s] and player1.bottom < HEIGHT:
        player1.y += PADDLE_SPEED
    if keys[pygame.K_UP] and player2.top > 0:
        player2.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
        player2.y += PADDLE_SPEED

    # Move the ball
    ball.x += BALL_SPEED_X
    ball.y += BALL_SPEED_Y

    # Ball collision with top/bottom
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        BALL_SPEED_Y *= -1

    # Ball collision with paddles
    if ball.colliderect(player1) or ball.colliderect(player2):
        BALL_SPEED_X *= -1

    # Power-up collision
    if powerup_visible and ball.colliderect(powerup_rect):
        powerup_visible = False
        if BALL_SPEED_X < 0:
            paddle = player1
        else:
            paddle = player2
        paddle.height += 20
        # Keep paddle within bounds
        if paddle.top < 0:
            paddle.top = 0
        if paddle.bottom > HEIGHT:
            paddle.bottom = HEIGHT
        powerup_timer = 0

    # Score and reset
    if ball.left <= 0:
        score2 += 1
        ball.center = (WIDTH // 2, HEIGHT // 2)
        BALL_SPEED_X *= -1
    if ball.right >= WIDTH:
        score1 += 1
        ball.center = (WIDTH // 2, HEIGHT // 2)
        BALL_SPEED_X *= -1

    # Handle power-up respawn
    if not powerup_visible:
        powerup_timer += dt
        if powerup_timer >= POWERUP_RESPAWN_TIME:
            powerup_rect.x = random.randint(20, WIDTH - 20 - POWERUP_SIZE)
            powerup_rect.y = random.randint(20, HEIGHT - 20 - POWERUP_SIZE)
            powerup_visible = True
            powerup_timer = 0

    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player1)
    pygame.draw.rect(screen, WHITE, player2)
    pygame.draw.ellipse(screen, WHITE, ball)
    if powerup_visible:
        pygame.draw.rect(screen, WHITE, powerup_rect)
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

    score_text = font.render(f"{score1} - {score2}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))

    pygame.display.flip()
