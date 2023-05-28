import pygame
import random
class Tank(pygame.sprite.Sprite):
    def __init__(self, x,y,size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size, size))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect(center=(x,y))
        self.speed = 3
        self.motion = 1

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,motion, speed=5):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5,5))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(center=(x, y))
        self.motion = motion
        self.speed = speed

    def update(self):
        if self.rect.x>500 or self.rect.x<0 or self.rect.y>500 or self.rect.y<0:
            self.kill
        if self.motion==1:
            self.rect.y -=self.speed
        if self.motion == 2:
            self.rect.x += self.speed
        if self.motion==3:
            self.rect.y +=self.speed
        if self.motion==4:
            self.rect.x -=self.speed

class Enemy (pygame.sprite.Sprite):
    def __init__(self, x=None, y=None, direction = None, speed = 3):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((20,20))
        self.image.fill((random.randint(0,255), random.randint(0,255),random.randint(0,255)))
        self.rect = self.image.get_rect(center=(x or random.randint(0,500), y or random.randint(0,500)))
        self.direction = direction or random.choice(('vertical', 'horizontal'))
        self.speed = speed

    def update(self):
        if self.direction == 'vertical':
            self.rect.y+=self.speed
            if self.rect.y>500:
                self.speed=-abs(self.speed)
            if self.rect.y<0:
                self.speed=abs(self.speed)
        elif self.direction == 'horizontal':
            self.rect.x += self.speed
            if self.rect.x > 500:
                self.speed = -abs(self.speed)
            if self.rect.x < 0:
                self.speed = abs(self.speed)

pygame.init() 
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption("TANK")
tank = Tank(40,80,40)

bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
font = pygame.font.Font('Halogen_0.ttf',20)
period_enemy=200
current_period_enemy=0
result =0
next_level=5

run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            tun = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                bullet_group.add(Bullet(tank.rect.centerx,tank.rect.centery,tank.motion ))

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        tank.rect.x-=tank.speed
        tank.motion= 4
    if key[pygame.K_RIGHT]:
        tank.rect.x += tank.speed
        tank.motion = 2
    if key[pygame.K_UP]:
        tank.rect.y -= tank.speed
        tank.motion = 1
    if key[pygame.K_DOWN]:
        tank.rect.y +=tank.speed
        tank.motion=3
    if current_period_enemy>=period_enemy:
        enemy_group.add(Enemy())
        current_period_enemy=0

    bullet_group.update()
    enemy_group.update()
    if pygame.sprite.spritecollide(tank, enemy_group,False):
        run = False
        print('collision!')
    if pygame.sprite.groupcollide(bullet_group, enemy_group, True, True):
        result+=1
        if result>=next_level:
            next_level+=5
            period_enemy/=2

    screen.fill((255,250,250))
    screen.blit(tank.image, tank.rect)
    bullet_group.draw(screen)
    enemy_group.draw(screen)
    screen.blit(font.render(f'Result: {result}', True, (0,0,0), (255,250,250)), (30,30))
    screen.blit(font.render(f'Score: {int(next_level/5)}', True, (0, 0, 0), (255, 250, 250)), (200, 30))
    pygame.display.flip()
    pygame.time.delay(20)
    current_period_enemy+=1
pygame.quit()
