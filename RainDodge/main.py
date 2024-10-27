import pygame
import time
import random
from typing import List

pygame.font.init()
WIDTH, HEIGHT = 1000, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rain Dodge")

PLAYER_WIDTH, PLAYER_HEIGHT = 40, 60
PLAYER_VOL = 5

FONT = pygame.font.SysFont("comicsans", 40)

BG = pygame.transform.scale(pygame.image.load("assets/bg.jpeg"), (WIDTH, HEIGHT))
def draw(player: pygame.Rect, stars: List[pygame.Rect], elapsed_time: float):
    WIN.blit(BG, (0, 0))
    time_text = FONT.render(f"Time elapsed: {round(elapsed_time)}s", 1, (255, 255, 255))
    WIN.blit(time_text, (WIDTH - time_text.get_width() - 10, 10))
    pygame.draw.rect(WIN, (255, 0, 0), player)
    for star in stars:
        pygame.draw.rect(WIN, "purple", star)
    pygame.display.update()



STAR_WIDTH = 10
STAR_HEIGHT = 10
STAR_VEL = 3

def main():
    run = True
    clock = pygame.time.Clock()
    start = time.time()
    elapsed_time = 0
    star_add_inc = 2000
    star_count = 0
    stars = []
    hit = False
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start
        if star_count > star_add_inc:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_inc = max(200, star_add_inc - 50)
            star_count = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x + PLAYER_VOL >= 0:
            player.x -= PLAYER_VOL
        elif keys[pygame.K_RIGHT] and player.x + PLAYER_VOL + PLAYER_WIDTH <= WIDTH:
            player.x += PLAYER_VOL
        elif keys[pygame.K_UP] and player.y + PLAYER_VOL >= 0:
            player.y -= PLAYER_VOL
        elif keys[pygame.K_DOWN] and player.y + PLAYER_VOL + PLAYER_HEIGHT <= HEIGHT:
            player.y += PLAYER_VOL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break
        if hit:
            lost_text = FONT.render("You Lost!", 1, "red")
            WIN.blit(lost_text, (WIDTH // 2 - lost_text.get_width() // 2, HEIGHT // 2 - lost_text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(4000)
            break


        draw(player, stars, elapsed_time)


    pygame.quit()

if __name__ == "__main__":
    main()