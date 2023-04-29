from random import randint
from pygame.locals import *
import pygame, time, sys

pygame.init()

pygame.display.set_caption("Racer")
W = 400
H = 600
SPEED = 2
SCORE = 0

WHITE = (255, 255, 255)


FPS = 60
FramePerSec = pygame.time.Clock()


game_over = pygame.font.SysFont("Verdana", 60).render("Game Over", True, (0, 0, 0))

background = pygame.image.load("road.jpg")

class Coin(pygame.sprite.Sprite):
    def __init__(self,scale, point):
        super().__init__()

        self.scale = scale
        self.point = point

        self.image = pygame.image.load("coin.jpg")
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * scale, self.image.get_height() * scale))

        self.rect = self.image.get_rect()
        self.rect.center=(randint(40,W-40),50) #creating coins

    
    def move(self):
        self.rect.move_ip(0,3) #coin speed
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (randint(30, 370), 0)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect) 

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("car2.jpg")
        self.rect = self.image.get_rect()
        self.rect.center=(randint(40,W-40),0) 
 
    def move(self):
        self.rect.move_ip(0,SPEED) #car speed move
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (randint(30, 370),0)
 
    def draw(self, surface):
        surface.blit(self.image, self.rect) 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("car1.jpg")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
 
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,5)
         
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < W:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
 
    def draw(self, surface):
        surface.blit(self.image, self.rect)     

Player1 = Player()
Enemy1 = Enemy()
Coin1 = Coin(1,2)
Coin2 = Coin(1.3,5)

#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(Enemy1)
coins = pygame.sprite.Group()
coins.add(Coin1)
coins.add(Coin2)
all_sprites = pygame.sprite.Group()
all_sprites.add(Player1)
all_sprites.add(Enemy1)
all_sprites.add(Coin1)
all_sprites.add(Coin2)

#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 5000)

sc = pygame.display.set_mode((W, H))

def coin_in(Coin):
    global SCORE 
    SCORE += Coin.point
    Coin.rect.top = 100
    Coin.rect.center = (randint(30, 370), -600 * Coin.point )
    pygame.display.update()
    

done = False
while not done: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == INC_SPEED:
              SPEED += 0.1
    
    sc.blit(background, (0,0))

    scores = pygame.font.SysFont("Verdana", 20).render(str(SCORE), True, (0, 0, 0))
    sc.blit(scores, (10,10))

    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        sc.blit(entity.image, entity.rect)
        entity.move()
    
    if pygame.sprite.collide_rect(Player1, Coin1):
        coin_in(Coin1)
        pygame.display.update()
    if pygame.sprite.collide_rect(Player1, Coin2):
        
        coin_in(Coin2)
        pygame.display.update()
    
    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(Player1, enemies):
        #sc.blit(scores, (200,350))    
        sc.blit(game_over, (30,250))

        pygame.display.update()

        time.sleep(1)

        for entity in all_sprites:
            entity.kill() 
          
        time.sleep(2)
        pygame.quit()
        sys.exit()
    pygame.display.update()
    FramePerSec.tick(FPS)
pygame.quit()