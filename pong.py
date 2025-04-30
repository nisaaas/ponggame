import pygame
import sys

# Inisialisasi Pygame
pygame.init()

# Konfigurasi layar
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (100, 100, 255)
BUTTON_HOVER_COLOR = (150, 150, 255)

# Paddle dan Bola
paddle_width, paddle_height = 15, 100
ball_size = 20

player1_x, player2_x = 50, WIDTH - 50 - paddle_width
player1_y, player2_y = HEIGHT // 2 - paddle_height // 2, HEIGHT // 2 - paddle_height // 2
ball_x, ball_y = WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2
ball_dx, ball_dy = 5, 5

paddle_speed = 10
ball_speed = 5

player1_score = 0
player2_score = 0
winning_score = 5  # Poin kemenangan

clock = pygame.time.Clock()

# Fungsi untuk menggambar elemen
def draw():
    screen.fill(BLACK)

    # Gambar paddles dan bola
    pygame.draw.rect(screen, WHITE, (player1_x, player1_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, WHITE, (player2_x, player2_y, paddle_width, paddle_height))
    pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, ball_size, ball_size))

    # Gambar skor
    font = pygame.font.SysFont(None, 36)
    player1_score_text = font.render(str(player1_score), True, WHITE)
    player2_score_text = font.render(str(player2_score), True, WHITE)

    # Menempatkan skor di layar
    screen.blit(player1_score_text, (WIDTH // 4 - player1_score_text.get_width() // 2, 20))
    screen.blit(player2_score_text, (WIDTH * 3 // 4 - player2_score_text.get_width() // 2, 20))

    pygame.display.update()

# Fungsi untuk menggambar layar start dengan tombol Play dan Exit
def draw_start_screen():
    screen.fill(BLACK)
    
    # Teks instruksi
    font = pygame.font.SysFont(None, 36)
    title_text = font.render("Pong Game", True, WHITE)
    instructions_text = font.render("Player 1: W (Up), S (Down)", True, WHITE)
    instructions2_text = font.render("Player 2: UP (Up), DOWN (Down)", True, WHITE)

    # Gambar teks ke layar
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
    screen.blit(instructions_text, (WIDTH // 2 - instructions_text.get_width() // 2, HEIGHT // 2 + 40))
    screen.blit(instructions2_text, (WIDTH // 2 - instructions2_text.get_width() // 2, HEIGHT // 2 + 80))

    # Tombol Play
    play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, 50)
    pygame.draw.rect(screen, BUTTON_COLOR, play_button)

    # Tombol Exit
    exit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 180, 200, 50)
    pygame.draw.rect(screen, BUTTON_COLOR, exit_button)

    # Teks untuk tombol
    play_text = font.render("Play", True, WHITE)
    exit_text = font.render("Exit", True, WHITE)
    screen.blit(play_text, (play_button.centerx - play_text.get_width() // 2, play_button.centery - play_text.get_height() // 2))
    screen.blit(exit_text, (exit_button.centerx - exit_text.get_width() // 2, exit_button.centery - exit_text.get_height() // 2))

    # Deteksi hover untuk efek tombol
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if play_button.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, play_button)
    if exit_button.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, exit_button)

    pygame.display.update()

    return play_button, exit_button

# Fungsi untuk menangani input dari tombol
def handle_button_click(play_button, exit_button):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    if mouse_pressed[0]:  # Jika klik kiri
        if play_button.collidepoint(mouse_x, mouse_y):
            return "play"
        if exit_button.collidepoint(mouse_x, mouse_y):
            return "exit"
    return None

# Fungsi untuk menggambar layar Game Over
def draw_game_over():
    screen.fill(BLACK)
    
    # Teks Game Over
    font = pygame.font.SysFont(None, 48)
    game_over_text = font.render("Game Over!", True, WHITE)
    winner_text = font.render(f"Player 1: {player1_score} - Player 2: {player2_score}", True, WHITE)
    
    # Teks untuk tombol
    play_again_text = font.render("Press ENTER to Play Again", True, WHITE)
    exit_text = font.render("Press ESC to Exit", True, WHITE)

    # Gambar teks ke layar
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))
    screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2))
    screen.blit(play_again_text, (WIDTH // 2 - play_again_text.get_width() // 2, HEIGHT // 2 + 40))
    screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 80))

    pygame.display.update()

# Fungsi utama untuk menjalankan game
def game_loop():
    global player1_y, player2_y, ball_x, ball_y, ball_dx, ball_dy

    while True:
        # Event handling untuk layar awal
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        play_button, exit_button = draw_start_screen()

        # Menangani klik tombol
        action = handle_button_click(play_button, exit_button)
        if action == "play":
            return  # Kembali ke game jika klik Play
        if action == "exit":
            pygame.quit()
            sys.exit()  # Keluar game jika klik Exit

        clock.tick(60)  # FPS

# Fungsi utama permainan
def play_game():
    global player1_y, player2_y, ball_x, ball_y, ball_dx, ball_dy, player1_score, player2_score

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Gerakan paddle
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player1_y > 0:
            player1_y -= paddle_speed
        if keys[pygame.K_s] and player1_y < HEIGHT - paddle_height:
            player1_y += paddle_speed
        if keys[pygame.K_UP] and player2_y > 0:
            player2_y -= paddle_speed
        if keys[pygame.K_DOWN] and player2_y < HEIGHT - paddle_height:
            player2_y += paddle_speed

        # Gerakan bola
        ball_x += ball_dx
        ball_y += ball_dy

        # Deteksi tabrakan bola dengan dinding
        if ball_y <= 0 or ball_y >= HEIGHT - ball_size:
            ball_dy = -ball_dy

        # Deteksi tabrakan bola dengan paddle
        if (ball_x <= player1_x + paddle_width and player1_y <= ball_y <= player1_y + paddle_height) or \
           (ball_x >= player2_x - ball_size and player2_y <= ball_y <= player2_y + paddle_height):
            ball_dx = -ball_dx

        # Deteksi jika bola keluar layar
        if ball_x <= 0:
            player2_score += 1  # Player 2 mendapat poin
            ball_x, ball_y = WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2
            ball_dx, ball_dy = -ball_dx, ball_dy
        elif ball_x >= WIDTH - ball_size:
            player1_score += 1  # Player 1 mendapat poin
            ball_x, ball_y = WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2
            ball_dx, ball_dy = -ball_dx, ball_dy

        # Cek jika salah satu pemain mencapai skor kemenangan
        if player1_score == winning_score or player2_score == winning_score:
            draw_game_over()

            # Tunggu untuk klik tombol Play Again atau Exit
            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:  # Play Again
                            player1_score = 0
                            player2_score = 0
                            return  # Kembali ke game loop untuk bermain lagi
                        if event.key == pygame.K_ESCAPE:  # Exit
                            pygame.quit()
                            sys.exit()

        draw()
        clock.tick(60)  # FPS

# Mulai game
game_loop()
play_game()
