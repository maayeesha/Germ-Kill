import pygame
import math
import random
from pygame import mixer

# Initializing Pygame
pygame.init()

# creating a screen
screen = pygame.display.set_mode((800, 600))
# Bckground
background = pygame.image.load("background.jpg")

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

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
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 8

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150)) # 480 -->good too
    enemyX_change.append(0.3)
    enemyY_change.append(40)



# Injection Drop
# Enemy
dropImg = pygame.image.load("drop.png")
dropX = 0
dropY = 520  # 480 -->good too
dropX_change = 0
dropY_change = 5  # 10 # as player is also at 520
drop_state = "ready"  # Ready -> you cannot see the drop on the screen,Shoot -> the drop will be moving

#score
score = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

#Game over text
over_font = pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
    score_value = font.render("Score: " + str(score),True,(255,255,255))
    screen.blit(score_value, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))  # blit basically means to draw


# Game loop {anything I want to be consistently shown while running the game goes to the while loop}

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def shoot_drop(x, y):
    global drop_state  # declaring this as global so that we can access the variable inside the function
    drop_state = "shoot"
    screen.blit(dropImg, (x + 16, y + 10))

def isCrash(enemyX, enemyY, dropX, dropY):
    distance = math.sqrt(math.pow(enemyX-dropX,2)+math.pow(enemyY-dropY,2))
    if distance < 27:
        return True
    else:
        return False

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
                    drop_sound = mixer.Sound('drop.wav')
                    drop_sound.play()


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
    for i in range(num_of_enemies):
        #Game Over
        if enemyY[i] > 460:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break


        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

            # Crash
        crash = isCrash(enemyX[i], enemyY[i], dropX, dropY)
        if crash:
            killed_sound = mixer.Sound('killed.wav')
            killed_sound.play()
            dropY = 520
            drop_state = "ready"
            score += 1
            print(score)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Drop Movement
    if dropY <= 0:
        dropY = 520
        drop_state = "ready"
    if drop_state == "shoot":
        shoot_drop(dropX, dropY)
        dropY -= dropY_change




    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()  # init,update is always gonna be there since it updates the game window
