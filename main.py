import pygame
import random

# Initializing Pygame
pygame.init()

# creating a screen
screen = pygame.display.set_mode((800, 600))
# Bckground
background = pygame.image.load("background.jpg")
# Title, icon
pygame.display.set_caption("Germ Kill")
icon = pygame.image.load("vaccine.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 520  # 480 -->good too
playerX_change = 0;

# Enemy
enemyImg = pygame.image.load("enemy.png")
enemyX = random.randint(0, 800)
enemyY = random.randint(50, 150)  # 480 -->good too
enemyX_change = 0.3
enemyY_change = 40

# Injection Drop
# Enemy
dropImg = pygame.image.load("drop.png")
dropX = 0
dropY = 520  # 480 -->good too
dropX_change = 0
dropY_change = 5  # 10 # as player is also at 520
drop_state = "ready"  # Ready -> you cannot see the drop on the screen,Shoot -> the drop will be moving


def player(x, y):
    screen.blit(playerImg, (x, y))  # blit basically means to draw


# Game loop {anything I want to be consistently shown while running the game goes to the while loop}

def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def shoot_drop(x, y):
    global drop_state  # declaring this as global so that we can access the variable inside the function
    drop_state = "shoot"
    screen.blit(dropImg, (x + 16, y + 10))


running = True
while running:

    screen.fill((0, 0, 0))
    # Background
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed check whether its left or right
        if event.type == pygame.KEYDOWN:  # pressing a keystroke
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5  # 0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5  # 0.3
            if event.key == pygame.K_SPACE:
                # get the current state coordinate of the doctor
                if drop_state == "ready":
                    dropX = playerX
                    shoot_drop(dropX, dropY)
        if event.type == pygame.KEYUP:  # releasing a keystroke
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Checking for boundaries

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736  # 736 why? Because screen width is 800 and player imae is 64 pixels and hece 800 - 64 = 736

    # germ will move
    enemyX += enemyX_change

    if enemyX <= 0:
        enemyX_change = 0.3
        enemyY += enemyY_change
    elif enemyX >= 736:
        enemyX_change = -0.3
        enemyY += enemyY_change

    # Drop Movement
    if dropY <= 0:
        dropY = 520
        drop_state = "ready"
    if drop_state == "shoot":
        shoot_drop(dropX, dropY)
        dropY -= dropY_change

    player(playerX, playerY)
    enemy(enemyX, enemyY)
    pygame.display.update()  # init,update is always gonna be there since it updates the game window
