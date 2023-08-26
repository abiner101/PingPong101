import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Configurações da tela
WIDTH = 800
HEIGHT = 600
BALL_SPEED = 5
PADDLE_SPEED = 7
WHITE = (255, 255, 255)
FPS = 60

# Inicialização da tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong Game")

# Inicialização dos objetos
ball = pygame.Rect(WIDTH/2 - 15, HEIGHT/2 - 15, 30, 30)
paddle1 = pygame.Rect(50, HEIGHT/2 - 70, 10, 140)
paddle2 = pygame.Rect(WIDTH - 60, HEIGHT/2 - 70, 10, 140)

# Velocidades iniciais da bola
ball_speed_x = BALL_SPEED
ball_speed_y = BALL_SPEED

# Velocidades dos jogadores
paddle1_speed = 0
paddle2_speed = 0

# Placar
score1 = 0
score2 = 0
font = pygame.font.Font(None, 36)

# Pontuação máxima
max_score = 10

clock = pygame.time.Clock()

# Função para reiniciar o jogo
def reset_game():
    global score1, score2
    ball.center = (WIDTH/2, HEIGHT/2)
    score1 = 0
    score2 = 0

# Loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Reiniciar o jogo
                reset_game()
            if event.key == pygame.K_UP:
                paddle2_speed = -PADDLE_SPEED
            if event.key == pygame.K_DOWN:
                paddle2_speed = PADDLE_SPEED
            if event.key == pygame.K_w:  # Tecla 'W' para subir a raquete do jogador 1
                paddle1_speed = -PADDLE_SPEED
            if event.key == pygame.K_s:  # Tecla 'S' para descer a raquete do jogador 1
                paddle1_speed = PADDLE_SPEED
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                paddle2_speed = 0
            if event.key == pygame.K_DOWN:
                paddle2_speed = 0
            if event.key == pygame.K_w:
                paddle1_speed = 0
            if event.key == pygame.K_s:
                paddle1_speed = 0

    # Atualizar lógica do jogo
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    paddle1.y += paddle1_speed
    paddle2.y += paddle2_speed

    # Colisões com as paredes
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y = -ball_speed_y

    # Colisão com as raquetes
    if ball.colliderect(paddle1) or ball.colliderect(paddle2):
        ball_speed_x = -ball_speed_x

    # Pontuação
    if ball.left <= 0:
        score2 += 1
        if score2 >= max_score:
            # Jogador 2 venceu
            reset_game()
        else:
            ball.center = (WIDTH/2, HEIGHT/2)
            ball_speed_x = BALL_SPEED
            ball_speed_y = BALL_SPEED
    if ball.right >= WIDTH:
        score1 += 1
        if score1 >= max_score:
            # Jogador 1 venceu
            reset_game()
        else:
            ball.center = (WIDTH/2, HEIGHT/2)
            ball_speed_x = -BALL_SPEED
            ball_speed_y = BALL_SPEED

    # Limitar movimento das raquetes dentro da tela
    paddle1.y = max(min(paddle1.y, HEIGHT - paddle1.height), 0)
    paddle2.y = max(min(paddle2.y, HEIGHT - paddle2.height), 0)

    # Desenhar na tela
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, WHITE, paddle1)
    pygame.draw.rect(screen, WHITE, paddle2)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH/2, 0), (WIDTH/2, HEIGHT))

    # Renderizar placar
    score_text = font.render(f"{score1} - {score2}", True, WHITE)
    screen.blit(score_text, (WIDTH/2 - score_text.get_width()/2, 10))

    pygame.display.flip()
    clock.tick(FPS)
