import math
from pygame import mixer
import pygame
from abc import ABC, abstractmethod

pygame.init()

screen = pygame.display.set_mode((800, 600))

backimage = pygame.image.load('background.png')

mixer.music.load('backgroundmusic.mp3')
pygame.mixer.music.play(-1)

pygame.display.set_caption("Mahantariksh ki Jung")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

def load_and_resize_image(path, scale):
    image = pygame.image.load(path)
    width = image.get_rect().width
    height = image.get_rect().height
    return pygame.transform.scale(image, (width * scale, height * scale))

player1Image = load_and_resize_image('spaceship.png', 1/10)
player2Image = load_and_resize_image('ufo.png', 1/10)
bulletImage = load_and_resize_image('bullet.png', 1/15)
thunderImage = load_and_resize_image('thunder.png', 1/15)

font = pygame.font.Font('god-of-war.ttf', 16)

class ProjectileState(ABC):
    @abstractmethod
    def update(self, projectile):
        pass

    @abstractmethod
    def fire(self, projectile):
        pass

class ReadyState(ProjectileState):
    def update(self, projectile):
        projectile.y = projectile.initial_y

    def fire(self, projectile):
        projectile.state = FiringState()
        projectile.x = projectile.owner.x
        return True

class FiringState(ProjectileState):
    def update(self, projectile):
        projectile.y += projectile.speed
        if projectile.y < -25 or projectile.y > 600:
            projectile.state = ReadyState()

    def fire(self, projectile):
        return False

class Projectile:
    def __init__(self, image, owner, speed, initial_y):
        self.image = image
        self.owner = owner
        self.speed = speed
        self.initial_y = initial_y
        self.x = 0
        self.y = initial_y
        self.state = ReadyState()

    def update(self):
        self.state.update(self)

    def fire(self):
        return self.state.fire(self)

    def draw(self, screen):
        if isinstance(self.state, FiringState):
            screen.blit(self.image, (self.x, self.y))

class Player:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.score = 0
        self.x_change = 0

    def move(self):
        self.x += self.x_change
        if self.x > 800:
            self.x = 0
        if self.x < 0:
            self.x = 800

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

player1 = Player(player1Image, 370, 530)
player2 = Player(player2Image, 200, 20)

bullet = Projectile(bulletImage, player1, -1.2, 480)
thunder = Projectile(thunderImage, player2, 1.2, 20)

def show_score(screen, font, player, player_num, x, y):
    score_text = font.render(f"Player {player_num} score: {player.score}", True, (255, 255, 255))
    screen.blit(score_text, (x, y))

def check_collision(projectile, target):
    distance = math.sqrt((target.x - projectile.x)**2 + (target.y - projectile.y)**2)
    return distance < 27

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(backimage, (0, 0))
    show_score(screen, font, player2, 2, 10, 5)
    show_score(screen, font, player1, 1, 640, 580)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player1.x_change = -1
            if event.key == pygame.K_RIGHT:
                player1.x_change = 1
            if event.key == pygame.K_a:
                player2.x_change = -1
            if event.key == pygame.K_d:
                player2.x_change = 1
            if event.key == pygame.K_UP:
                if bullet.fire():
                    bullet_sound = mixer.Sound('bullet_sound.wav')
                    bullet_sound.play()
            if event.key == pygame.K_w:
                if thunder.fire():
                    thunder_sound = mixer.Sound('thunder_sound.wav')
                    thunder_sound.play()
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                player1.x_change = 0
            if event.key in (pygame.K_a, pygame.K_d):
                player2.x_change = 0

    player1.move()
    player2.move()
    bullet.update()
    thunder.update()

    if check_collision(bullet, player2):
        explosion_sound = mixer.Sound('explosion.wav')
        explosion_sound.play()
        bullet.state = ReadyState()
        player1.score += 1

    if check_collision(thunder, player1):
        explosion_sound = mixer.Sound('explosion.wav')
        explosion_sound.play()
        thunder.state = ReadyState()
        player2.score += 1

    player1.draw(screen)
    player2.draw(screen)
    bullet.draw(screen)
    thunder.draw(screen)

    pygame.display.update()

print("Player 1 score is:", player1.score)
print("Player 2 score is:", player2.score)

pygame.quit()
