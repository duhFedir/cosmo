import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 Space Shooter (Easy Mode)")
clock = pygame.time.Clock()

WHITE = (255,255,255)
RED = (255,0,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)

try:
    player_img = pygame.image.load("shuttle.png")
except:
    player_img = pygame.Surface((50, 50))
    player_img.fill(YELLOW)

player_img = pygame.transform.scale(player_img, (50, 50))
player = player_img.get_rect(center=(WIDTH//2, HEIGHT-60))

player_speed = 10
bullets = []
enemies = []
score = 0
hp = 10
weapon = 3

font = pygame.font.SysFont(None, 30)

ENEMY_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ENEMY_EVENT, 1200)

running = True
while running:
    clock.tick(60)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == ENEMY_EVENT:
            enemies.append([random.randint(0, WIDTH-30), -30, 30, random.randint(1,3)])

        if event.type == pygame.MOUSEBUTTONDOWN:
            if weapon == 1:
                bullets.append([player.centerx, player.top, 0])
            elif weapon == 2:
                bullets.append([player.centerx-10, player.top, 0])
                bullets.append([player.centerx+10, player.top, 0])
            elif weapon == 3:
                bullets.append([player.centerx, player.top, 0])
                bullets.append([player.centerx, player.top, -3])
                bullets.append([player.centerx, player.top, 3])

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: weapon = 1
            if event.key == pygame.K_2: weapon = 2
            if event.key == pygame.K_3: weapon = 3

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player.x += player_speed

    if player.left < 0: player.left = 0
    if player.right > WIDTH: player.right = WIDTH

    for b in bullets[:]:
        b[1] -= 12
        b[0] += b[2]  

        if b[1] < 0 or b[0] < 0 or b[0] > WIDTH:
            bullets.remove(b)

    for e in enemies[:]:
        e[1] += e[3]
        enemy_rect = pygame.Rect(e[0], e[1], e[2], e[2])

        if e[1] > HEIGHT:
            enemies.remove(e)
            hp -= 1

        if player.colliderect(enemy_rect):
            enemies.remove(e)
            hp -= 1

        for b in bullets[:]:
            if enemy_rect.collidepoint(b[0], b[1]):
                if e in enemies: enemies.remove(e)
                if b in bullets: bullets.remove(b)
                score += 1
                break

    screen.blit(player_img, player)

    for b in bullets:
        pygame.draw.rect(screen, YELLOW, (b[0], b[1], 4, 10))

    for e in enemies:
        pygame.draw.rect(screen, RED, (e[0], e[1], e[2], e[2]))

    screen.blit(font.render(f"Score: {score}", True, WHITE), (10,10))
    hp_color = RED if hp <= 3 else WHITE
    screen.blit(font.render(f"HP: {hp}", True, hp_color), (10,40))
    screen.blit(font.render(f"Weapon: {weapon}", True, WHITE), (10,70))

    if hp <= 0:
        over_font = pygame.font.SysFont(None, 72)
        screen.blit(over_font.render("GAME OVER", True, RED), (WIDTH//2-140, HEIGHT//2-30))
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False

    pygame.display.flip()

pygame.quit()