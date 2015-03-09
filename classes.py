__author__ = 'Simon'
from config import *


class Castle(pygame.sprite.Sprite):

    def __init__(self, manager):
        pygame.sprite.Sprite.__init__(self)
        self.manager = manager
        self.surface = self.manager.surface
        self.image = pygame.image.load("castle.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = width*3/4
        self.rect.y = height*3/4

    def draw(self):
        self.surface.blit(self.image, self.rect)


class Enemy(pygame.sprite.Sprite):

    def __init__(self, manager, speed, health):
        pygame.sprite.Sprite.__init__(self)
        self.manager = manager
        self.speed = speed
        self.health = health
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
        self.money_counter = eztext.Input(maxlength=45, color=(255, 255, 255), prompt='money: '+str(self.manager.money))
        self.timer = 0

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for enemy in self.enemies:
                if enemy.rect.collidepoint(x, y):
                    enemy.health -= 1
                    if enemy.health <= 0:
                        enemy.kill()
                        self.manager.money += 100
        if event.type == pygame.KEYDOWN:
            self.manager.end_game()

    def draw(self):
        self.castle.draw()
        self.enemies.draw(self.surface)

    def update(self):

        self.timer += 1
        if self.timer >= 100:
            enemy = Enemy(self, 1, 2)
            self.enemies.add(enemy)
            self.timer = 0
        for enemy in self.enemies:
            enemy.move()


class Game():

    def __init__(self, surface):
        self.surface = surface
        self.money = int(saved_money)
        self.screen = GameScreen(self.surface, self)
        self.money_counter = eztext.Input(maxlength=45, color=white, prompt='money: '+str(self.money))

    def draw(self):
        self.screen.draw()
        self.money_counter.draw(self.surface)

    def handle_events(self, event):
        self.screen.handle_events(event)

    def end_game(self):
        saved_data[0] = self.money
        f = open('saved_data', 'w')
        json.dump(saved_data, f)
        f.close()
        sys.exit(0)

    def update(self):
        self.money_counter = eztext.Input(maxlength=45, color=white, prompt='money: '+str(self.money))
        self.screen.update()