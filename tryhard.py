import pygame
import math
import random
from pygame import mixer

#  Initializing Pygame
pygame.init()

# create the game
screen = pygame.display.set_mode((800,600))

# Title and Icon
pygame.display.set_caption("Tutorial")
icon = pygame.image.load('laughing.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('background.png')

#Background Sound
mixer.music.load('hype.mp3')
mixer.music.play(-1)

# Player
player_img =  pygame.image.load('banana.png')
playerX = 370
playerY = 480
playerX_change = 0

# Score 
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10
def show_score(x,y):
    score = font.render('Score : ' + str(score_value), True, (255,255,255))
    screen.blit(score,(x,y))

def player(x,y):
    screen.blit(player_img,(x,y))

enemy_img =  []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

# Enemy
for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(2)
    enemyY_change.append(100)

def enemy(x,y,i):
    screen.blit(enemy_img[i],(x,y))

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf',64)

def game_over_text():
    over_score = over_font.render(f'MAR GAYA MC', True, (255,255,255))
    screen.blit(over_score,(200,250))

# Bullet

# Ready - You cant see the bullet on the screen
# Fire - The bullet is currently moving
bullet_img =  pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 7
bullet_state = "ready"
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img,(x+16,y+10))

# Distance between two points and the midpoint
# D = √(x2−x1)2+(y2−y1)2
def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

# Game Loop
running = True
while running:
    screen.fill((0,0,0))  # Backgound Colours # RGB (RED, GREEN, BLUE)
    #Background image
    screen.blit(background,(0,0))

    # playerX += 0.1 # To change cordinates of things to make them move

    for i in pygame.event.get():
        if i.type == pygame.QUIT: # for quiting the 
            running = False
    
    # if keystroke is pressed check whether its right or left
        if i.type == pygame.KEYDOWN:
            # print('A keystroke is pressed')
            if i.key == pygame.K_LEFT:
                playerX_change = -4
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_RIGHT:
                playerX_change = 4
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_SPACE:
                # get the current X cordinate of the spaceship
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('boom.mp3')
                    bullet_sound.play() 
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)
        if i.type == pygame.KEYUP:
            if i.key == pygame.K_LEFT or i.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    # Adding boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    

    # Adding boundaries
    # Enemies movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 470:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]
    
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('enemy.mp3')
            explosion_sound.play() 
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)
        enemy(enemyX[i],enemyY[i],i)
    
    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state == 'fire':
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change

    show_score(textX,textY)
    player(playerX,playerY)
    pygame.display.update() # used after events to update the program