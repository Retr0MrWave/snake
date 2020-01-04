import pygame
import random

def sign(n):
    if n > 0:
        return 1
    if n < 0:
        return -1
    if n == 0:
        return 0

def collision(a, b):
    return a.topleft == b.topleft

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

DIRECTIONS = [[0, 1], [1, 0], [0, -1], [-1, 0]]
d = [1]

snake = [pygame.Rect((0, 0), (16, 16))]
randx = random.randint(0, 15)
randy = random.randint(0, 15)
bonus = pygame.Rect((16 * randx, 16 * randy), (16 * (randx+1), 16 * (randy+1)))

f = True
while f:
    try:
        difficulty = int(input("Enter difficulty (1 - easy, 2 - medium, 3 - hard): "))
    except ValueError:
        difficulty = 0
    if difficulty == 1:
        diff = 60
        f = False
    elif difficulty == 2:
        diff = 30
        f = False
    elif difficulty == 3:
        diff = 15
        f = False
    else:
        print("Unknown difficulty. You need to enter 1, 2 or 3")

pygame.init()

screen = pygame.display.set_mode((16*16, 16*16))
pygame.display.set_caption("Snake")
screen_rect=screen.get_rect()

clock = pygame.time.Clock()

snakeSurface = pygame.Surface((16, 16))
bonusSurface = pygame.Surface((16, 16))

snakeSurface.fill(RED)
bonusSurface.fill(GREEN)

time = 0
c = 1
while True:
    clock.tick(60)

    if time % diff == 0:
        # Move our snake
        if c < len(snake):
            for i in range(len(snake)):
                snake[i].move_ip(DIRECTIONS[d[i]][0] * 16, DIRECTIONS[d[i]][1] * 16)
            d[c] = d[c-1]
            c += 1
        else:
            for cell in snake:
                cell.move_ip(DIRECTIONS[d[0]][0] * 16, DIRECTIONS[d[0]][1] * 16)

        # Check colisions
        for cell in snake[2:]:
            if collision(snake[0], cell):
                pygame.quit()
                print("You lost. Your score:", len(snake))
                input("Press enter to continue.")
                quit()
        if not(screen_rect.contains(snake[0])):
                pygame.quit()
                print("You lost. Your score:", len(snake))
                input("Press enter to continue.")
                quit()

        if collision(snake[0], bonus):
            if len(snake) > 1:
                newx = snake[-1].x + (DIRECTIONS[(d[-1]+2)%4][0] * 16)
                newy = snake[-1].y + (DIRECTIONS[(d[-1]+2)%4][1] * 16)
            else:
                newx = snake[0].x + DIRECTIONS[(d[0]+2)%4][0]*16
                newy = snake[0].y + DIRECTIONS[(d[0]+2)%4][1]*16
            newCell = pygame.Rect((newx, newy), (newx+16, newy+16))
            d.append(d[-1])
            snake.append(newCell)

            randx = random.randint(0, 15)
            randy = random.randint(0, 15)
            bonus = pygame.Rect((16 * randx, 16 * randy), (16 * (randx+1), 16 * (randy+1)))
    
    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if d[0] != 0:
                    d[0] = 2
                    c = 1
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if d[0] != 2:
                    d[0] = 0
                    c = 1
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if d[0] != 1:
                    d[0] = 3
                    c = 1
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if d[0] != 3:
                    d[0] = 1
                    c = 1

    # Screen update
    screen.fill(BLACK)
    screen.blit(bonusSurface, bonus)
    for cell in snake:
        screen.blit(snakeSurface, cell)
    pygame.display.update()

    time += 1