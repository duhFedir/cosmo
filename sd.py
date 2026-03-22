import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 Space Shooter ULTRA (Pygame)")
clock = pygame.time.Clock()

# colors
WHITE = (255,255,255)
RED = (255,0,0)
CYAN = (0,255,255)
YELLOW = (255,255,0)
GREEN = (0,255,0)
PURPLE = (180,0,255)
BLACK = (0,0,0)
ORANGE = (255,150,0)

# player
player = pygame.Rect(WIDTH//2, HEIGHT-60, 40, 40)
player_speed = 6

bullets = []
enemies = []
bonuses = []
particles = []
stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1,3)] for _ in range(80)]

score = 0
hp = 3
shoot_mode = 1

font = pygame.font.SysFont(None, 30)

# timers
ENEMY_EVENT = pygame.USEREVENT + 1
BONUS_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(ENEMY_EVENT, 700)
pygame.time.set_timer(BONUS_EVENT, 5000)


def create_explosion(x, y):
    for _ in range(15):
        particles.append([x, y, random.uniform(-3,3), random.uniform(-3,3), 30])


running = True
while running:
    clock.tick(60)
    screen.fill(BLACK)

    # stars background
    for s in stars:
        s[1] += s[2]
        if s[1] > HEIGHT:
            s[0] = random.randint(0, WIDTH)
            s[1] = 0
        pygame.draw.rect(screen, WHITE, (s[0], s[1], 2, 2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == ENEMY_EVENT:
            size = 20 if random.random() < 0.8 else 40
            hp_enemy = 1 if size == 20 else 3
            speed = random.randint(2,4) if size == 20 else 1
            enemies.append([random.randint(0, WIDTH), -20, size, speed, hp_enemy])

        if event.type == BONUS_EVENT:
            bonuses.append([random.randint(0, WIDTH), -20, random.choice(['heal','gun'])])

        if event.type == pygame.MOUSEBUTTONDOWN:
            if shoot_mode == 1:
                bullets.append([player.centerx, player.top])
            else:
                bullets.append([player.centerx-10, player.top])
                bullets.append([player.centerx+10, player.top])

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player.x += player_speed

    # bullets
    for b in bullets[:]:
        b[1] -= 8
        if b[1] < 0:
            bullets.remove(b)

    # enemies
    for e in enemies[:]:
        e[1] += e[3]

        if e[1] > HEIGHT:
            enemies.remove(e)
            hp -= 1

        if player.colliderect(pygame.Rect(e[0], e[1], e[2], e[2])):
            enemies.remove(e)
            hp -= 1
            create_explosion(player.centerx, player.centery)

        for b in bullets[:]:
            if pygame.Rect(e[0], e[1], e[2], e[2]).collidepoint(b[0], b[1]):
                e[4] -= 1
                bullets.remove(b)
                if e[4] <= 0:
                    enemies.remove(e)
                    create_explosion(e[0], e[1])
                    score += 1

    # bonuses
    for b in bonuses[:]:
        b[1] += 2
        rect = pygame.Rect(b[0], b[1], 15, 15)

        if player.colliderect(rect):
            if b[2] == 'heal': hp += 1
            if b[2] == 'gun': shoot_mode = 2
            bonuses.remove(b)

    # particles
    for p in particles[:]:
        p[0] += p[2]
        p[1] += p[3]
        p[4] -= 1
        if p[4] <= 0:
            particles.remove(p)

    # draw player
    pygame.draw.rect(screen, CYAN, player)

    # draw bullets
    for b in bullets:
        pygame.draw.rect(screen, YELLOW, (b[0], b[1], 4, 10))

    # draw enemies
    for e in enemies:
        pygame.draw.rect(screen, RED, (e[0], e[1], e[2], e[2]))

    # draw bonuses
    for b in bonuses:
        color = GREEN if b[2]=='heal' else PURPLE
        pygame.draw.rect(screen, color, (b[0], b[1], 15, 15))

    # draw particles
    for p in particles:
        pygame.draw.rect(screen, ORANGE, (p[0], p[1], 3, 3))

    # UI
    score_text = font.render(f"Score: {score}", True, WHITE)
    hp_text = font.render(f"HP: {hp}", True, WHITE)
    screen.blit(score_text, (10,10))
    screen.blit(hp_text, (10,40))

    if hp <= 0:
        game_over = font.render("GAME OVER", True, RED)
        screen.blit(game_over, (WIDTH//2-80, HEIGHT//2))
        pygame.display.flip()
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()

    pygame.display.flip()
