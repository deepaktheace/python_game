import pygame
from pygame import mixer
from random import randint
from math import sqrt,pow
#intialize pygame
pygame.init()

#setting screen
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Retro Space Invaders")
icon = pygame.image.load('images/ufoIcon.png')
pygame.display.set_icon(icon)
space = pygame.image.load('images/space.png')
background = pygame.transform.scale(space,(800,600))

#Music and Sound Effect
mixer.music.load('music/Background.wav')
mixer.music.play(-1)

#Player
playerImg = pygame.image.load('images/player2.png')
playerX = 370
playerY = 480
playerX_change = 0
playerImgNew = pygame.transform.scale(playerImg,(64,64))
def player(x,y):
    screen.blit(playerImgNew,(x,y))

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemyImgNew = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('images/alien.png'))
    enemyX.append(randint(8,728))
    enemyY.append(randint(50,150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)
    enemyImgNew.append(pygame.transform.scale(enemyImg[i],(64,64)))
    def enemy(x,y,i):
        screen.blit(enemyImgNew[i],(x,y))

#Bullet
bulletImg = pygame.image.load('images/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1.5
bullet = pygame.transform.scale(bulletImg,(42,42))
bullet_state = "ready"  
def fire(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet,(x+16,y+10))

def collide(enemyX,enemyY,bulletX,bulletY):
    distance = sqrt((pow(enemyX-bulletX,2))+(pow(enemyY-bulletY,2)))
    if distance < 27 :
        return True
    else:
        return False
#Score
score_value = 0
highscore_value = 0 
font = pygame.font.Font('freesansbold.ttf',32)
def display_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255,255,255))
    screen.blit(score,(x,y))

#Game Over
over_font = pygame.font.Font('freesansbold.ttf',64)
def game_over():
    over_text  = over_font.render("GAME OVER",True,(255,0,0))
    screen.blit(over_text,(200,250))

#Game loop
running = True
FPS = 420
clock = pygame.time.Clock()
while running:
    clock.tick(FPS) 
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #Key events 
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX_change = -0.3
        if event.key == pygame.K_RIGHT:
            playerX_change = 0.3
        if event.key == pygame.K_LCTRL or event.key == pygame.K_UP :
            if bullet_state == "ready":
                bullet_Sound = mixer.Sound('music/Laser.wav')
                bullet_Sound.play()
                bulletX = playerX
                fire(bulletX,bulletY)
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
            playerX_change = 0
    
    #Player boundries
    playerX += playerX_change
    if playerX <= 8:
        playerX = 8
    if playerX >= 728:
        playerX = 728

    #Enemy movement
    for i in range(num_of_enemies):

        if enemyY[i] > 440:
            mixer.music.stop()
            gameOver_Sound = mixer.Sound('music/GameOver.wav')
            gameOver_Sound.play(1)
            
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            break    

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 8:
            enemyX_change[i] = 0.3
            enemyY[i] +=  enemyY_change[i]
        elif enemyX[i] >= 728:
            enemyX_change[i] = -0.3
            enemyY[i] +=  enemyY_change[i]

        #Collision
        collision = collide(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            collision_Sound = mixer.Sound('music/Collision.wav')
            collision_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = randint(8,728)
            enemyY[i] = randint(50,150)

        enemy(enemyX[i],enemyY[i], i)

    #Bullet movement
    if bulletY <= 0 :
        bulletY= 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire(bulletX,bulletY)
        bulletY -= bulletY_change
    
    player(playerX,playerY)
    display_score(10,10)
    pygame.display.update()