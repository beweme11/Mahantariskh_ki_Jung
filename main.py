import math
from pygame import mixer
import pygame
import math


# intializes the game package
pygame.init()

# creates the screen
screen = pygame.display.set_mode((800, 600))

# background
backimage = pygame.image.load('background.png')

# background music
mixer.music.load('backgroundmusic.mp3')
pygame.mixer.music.play(-1)




# title and icon
pygame.display.set_caption("Mahantariksh ki Jung")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# player1 image resizing and loading
image = pygame.image.load('spaceship.png')
width = image.get_rect().width
height = image.get_rect().height

player1Image = pygame.transform.scale(image, (width * (1 / 10), height * (1 / 10)))
player1X = 370
player1Y = 530
player1Y_change = 0
player1X_change = 0

player1_score = 0
player2_score = 0


def player1(x, y):
    screen.blit(player1Image, (x, y))


# player2 image resizing and loading

image2 = pygame.image.load('ufo.png')
width = image2.get_rect().width
height = image2.get_rect().height
player2Image = pygame.transform.scale(image2, (width * (1 / 10), height * (1 / 10)))
player2X = 200
player2Y = 20
player2X_change = 0
player2Y_change = 0


def player2(x, y):
    screen.blit(player2Image, (x, y))


# display score on screen

font = pygame.font.Font('god-of-war.ttf', 16)
etextX = 10
etextY = 5
ptextX = 640
ptextY = 580

def show_player1_score(x, y):
    player1score = font.render("player 1 score :" + str(player1_score), True, (255, 255, 255))
    screen.blit(player1score, (x, y))


def show_player2_score(x, y):
    player2score = font.render("player 2 score :" + str(player2_score), True, (255, 255, 255))
    screen.blit(player2score, (x, y))


# bullet image loading and resizing
image3 = pygame.image.load('bullet.png')
width = image3.get_rect().width
height = image3.get_rect().height
bulletImage = pygame.transform.scale(image3, (width * (1 / 15), height * (1 / 15)))
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1.2
# state= fire means in action and visible, ready means not in action and invisible
bullet_state = "ready"

# thunder image loading and resizing
image4 = pygame.image.load('thunder.png')
width = image4.get_rect().width
height = image4.get_rect().height
thunderImage = pygame.transform.scale(image4, (width * (1 / 15), height * (1 / 15)))
thunderX = 0
thunderY = 20
thunderX_change = 0
thunderY_change = -1.2

# state= fire means in action and visible, ready means not in action and invisible
thunder_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImage, (x + 8, y + 25))


def fire_thunder(x, y):
    global thunder_state
    thunder_state = "fire"
    screen.blit(thunderImage, (x, y))


def collision(player2X, player2Y, player1X, player1Y):
    distance = math.sqrt(math.pow((player2X - bulletX), 2)) + (math.pow((player2Y - bulletY), 2))

    if distance < 27:
        return True
    else:
        return False


def collison2():
    distance2 = math.sqrt(math.pow((player1X - thunderX), 2)) + (math.pow((player1Y - thunderY), 2))

    if distance2 < 27:
        return True
    else:
        return False

    # game window infinite loop


# game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(backimage, (0, 0))
    show_player2_score(etextX, etextY)
    show_player1_score(ptextX, ptextY)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # check if key is pressed and change position of player1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player1X_change = -0.3
            if event.key == pygame.K_RIGHT:
                player1X_change = +0.3

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player2X_change = -0.3
            if event.key == pygame.K_d:
                player2X_change = +0.3

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if bullet_state == "ready":
                    bulletX = player1X
                    fire_bullet(bulletX, bulletY)
                bullet_sound = mixer.Sound('bullet_sound.wav')
                bullet_sound.play()

            if event.key == pygame.K_w:
                if thunder_state == "ready":
                    thunderX = player2X
                    fire_thunder(thunderX, thunderY)
                thunder_sound = mixer.Sound('thunder_sound.wav')
                thunder_sound.play()

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if thunder_state is "fire":
        fire_thunder(thunderX, thunderY)
        thunderY -= thunderY_change

    # repositioning to extremes
    if bulletY < -25:
        bullet_state = "ready"
        bulletY = player1Y - 10
    if thunderY > 600:
        thunder_state = "ready"
        thunderY = player2Y + 10
    if player1X > 800:
        player1X = 0
    if player1X < 0:
        player1X = 800

    if player2X > 800:
        player2X = 0
    if player2X < 0:
        player2X = 800

    # collision
    hascollision = collision(player2X, player2Y, bulletX, bulletY)
    if hascollision:
        explosion_sound = mixer.Sound('explosion.wav')
        explosion_sound.play()
        bulletY = player1Y - 10
        bullet_state = "ready"
        player1_score += 1


    # collison 2
    hascollision2 = collison2()
    if hascollision2:
        explosion_sound = mixer.Sound('explosion.wav')
        explosion_sound.play()
        thunderY = player2Y + 10
        thunder_state = "ready"
        player2_score += 1


    player1X += player1X_change
    player1Y += player1Y_change

    player1(player1X, player1Y)

    player2X += player2X_change
    player2Y += player2Y_change

    player2(player2X, player2Y)

    pygame.display.update()
print("player1 score is : ", player1_score)
print("player2 score is : ", player2_score)
