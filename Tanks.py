import pygame
import random
import glob
import json

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3
        self.motion = 1

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, motion, speed=5):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 5))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.motion = motion
        self.speed = speed

    def update(self):
        if self.rect.x > 700 or self.rect.x < 0 or self.rect.y > 500 or self.rect.y < 0:
            self.kill()
        if self.motion == 1:
            self.rect.y -= self.speed
        if self.motion == 2:
            self.rect.x += self.speed
        if self.motion == 3:
            self.rect.y += self.speed
        if self.motion == 4:
            self.rect.x -= self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x=None, y=None, direction=None, speed=3, safe_zone=50):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        x = x or random.randint(50, 450)
        y = y or random.randint(50, 450)
        while abs(x - 40) < safe_zone and abs(y - 80) < safe_zone:
            x = random.randint(50, 450)
            y = random.randint(50, 450)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction or random.choice(('vertical', 'horizontal'))
        self.speed = speed


    def update(self):
        if self.direction == 'vertical':
            self.rect.y += self.speed
            if self.rect.y > 500:
                self.speed = -abs(self.speed)
            if self.rect.y < 0:
                self.speed = abs(self.speed)
        elif self.direction == 'horizontal':
            self.rect.x += self.speed
            if self.rect.x > 700:
                self.speed = -abs(self.speed)
            if self.rect.x < 0:
                self.speed = abs(self.speed)

def load_scores():
    try:
        with open('scores.json', 'r') as file:
            scores = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        scores = [0, 0, 0]

    return scores

def update_scores(result, scores):
    scores.append(result)
    scores.sort(reverse=True)
    scores = scores[:3]

    with open('scores.json', 'w') as file:
        json.dump(scores, file)

    return scores


def skin_selection(screen, font):
    skins = glob.glob("*.png")
    skin_dict = {str(i + 1): pygame.transform.scale(pygame.image.load(skin), (40, 40)) for i, skin in enumerate(skins)}
    skin_dict['0'] = pygame.Surface((40, 40))
    skin_dict['0'].fill((0, 0, 0))
    skin_choice = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    skin_choice = (skin_choice + 1) % len(skin_dict)
                elif event.key == pygame.K_LEFT:
                    skin_choice = (skin_choice - 1) % len(skin_dict)
                elif event.key == pygame.K_RETURN:
                    return skin_dict[str(skin_choice)]

        screen.fill((255, 250, 250))
        screen.blit(font.render(f"Choose skin: ", True, (0, 0, 0), (255, 250, 250)), (10, 10))
        screen.blit(skin_dict[str(skin_choice)], (200, 200))
        pygame.display.flip()


def end_screen(result, scores, screen, font):
    run = True
    while run:
        screen.fill((255, 250, 250))
        screen.blit(font.render(f'Game over!', True, (0, 0, 0), (255, 250, 250)), (300, 150))
        final_score = font.render(f'Your result: {result}', True, (0, 0, 0), (255, 250, 250))
        best_scores = font.render(f'Best results: {scores}', True, (0, 0, 0), (255, 250, 250))
        screen.blit(final_score, (200, 200))
        screen.blit(best_scores, (200, 230))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
        pygame.display.flip()

def main(screen, font):
    tank_skin = skin_selection(screen, font)
    tank = Tank(40, 80, tank_skin) 
    bullet_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    period_enemy = 200
    current_period_enemy = 0
    result = 0
    next_level = 5
    speed_enemy = 2
    scores = load_scores()
    run = True

    while run:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    bullet_group.add(Bullet(tank.rect.centerx, tank.rect.centery, tank.motion))

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            tank.rect.x -= tank.speed
            tank.motion = 4
        if key[pygame.K_RIGHT]:
            tank.rect.x += tank.speed
            tank.motion = 2
        if key[pygame.K_UP]:
            tank.rect.y -= tank.speed
            tank.motion = 1
        if key[pygame.K_DOWN]:
            tank.rect.y += tank.speed
            tank.motion = 3
        if current_period_enemy >= period_enemy:
            enemy_group.add(Enemy(speed=speed_enemy))
            current_period_enemy = 0

        bullet_group.update()
        enemy_group.update()
        if pygame.sprite.spritecollide(tank, enemy_group, False):
            run = False
            scores = update_scores(result, scores)
        if pygame.sprite.groupcollide(bullet_group, enemy_group, True, True):
            result += 1
            if result >= next_level:
                next_level += 5
                speed_enemy += 1
                period_enemy /= 2

        screen.fill((255, 250, 250))
        screen.blit(tank.image, tank.rect)
        bullet_group.draw(screen)
        enemy_group.draw(screen)
        screen.blit(font.render(f'Your result: {result}', True, (0, 0, 0), (255, 250, 250)), (10, 10))
        screen.blit(font.render(f'Best results: {scores}', True, (0, 0, 0), (255, 250, 250)), (10, 30))
        current_period_enemy += 1
        pygame.display.flip()
        pygame.time.delay(16)
    end_screen(result, scores, screen, font)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((700, 500))
    pygame.display.set_caption("TANK")
    font = pygame.font.Font('Halogen_0.ttf', 20)
    main(screen, font)
    pygame.quit()