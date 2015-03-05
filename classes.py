__author__ = 'Simon'
from config import *


class Castle(pygame.sprite.Sprite):

    def __init__(self, manager):
        pygame.sprite.Sprite.__init__(self)
        self.manager = manager
        self.surface = self.manager.surface
        self.image = pygame.image.load("castle.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 600
        self.rect.y = 450

    def draw(self):
        self.surface.blit(self.image, self.rect)


class Enemy(pygame.sprite.Sprite):

    def __init__(self, manager, speed):
        pygame.sprite.Sprite.__init__(self)
        self.manager = manager
        self.speed = speed
        self.surface = self.manager.surface
        self.image = pygame.image.load("enemy.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 500

    def move(self):
        if not pygame.sprite.collide_rect(self, self.manager.castle):
            self.rect.x += self.speed


class GameScreen():

    def __init__(self, surface, manager):
        self.surface = surface
        self.manager = manager
        self.castle = Castle(self.manager)
        self.enemies = pygame.sprite.Group()

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for enemy in self.enemies:
                if enemy.rect.collidepoint(x, y):
                    enemy.kill()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                enemy = Enemy(self, 1)
                self.enemies.add(enemy)

    def draw(self):
        self.castle.draw()
        self.enemies.draw(self.surface)

    def update(self):
        for enemy in self.enemies:
            enemy.move()


class Game():

    def __init__(self, surface):
        self.surface = surface
        self.screen = GameScreen(self.surface, self)
        self.money = 0

    def draw(self):
        self.screen.draw()

    def handle_events(self, event):
        self.screen.handle_events(event)

    def end_game(self):
        f = open('high_scores', 'r')
        my_money = json.load(f)

        gained_money = self.money
        my_money += gained_money

        f = open('high_scores', 'w')
        json.dump(my_money, f)
        f.close()
        sys.exit(0)

    def update(self):
        self.screen.update()